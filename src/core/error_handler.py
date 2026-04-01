from functools import wraps
from enum import Enum, auto
from typing import Type, List

import comtypes

from src.core.logger import get_logger


logger = get_logger(__name__)

class RTDConnectionState(Enum):
    """Enum representing the possible connection states of the RTD update event handler."""
    DISCONNECTED = auto()
    CONNECTED = auto()
    CONNECTING = auto()
    DISCONNECTING = auto()

class RTDError(Exception):
    """Base exception class for all RTD-related errors."""
    def __init__(self, message: str, *args):
        super().__init__(message, *args)
        logger.error(f"{self.__class__.__name__}: {message}")

class RTDUpdateError(RTDError):
    """Exception raised for errors related to RTD updates."""
    pass

class RTDConnectionError(RTDError):
    """Exception raised for errors related to RTD connection state changes."""
    pass

class RTDHeartbeatError(RTDError):
    """Exception raised for errors related to RTD heartbeat operations."""
    pass

class RTDServerError(RTDError):
    """Exception raised for errors related to RTD server operations."""
    pass

class RTDClientError(RTDError):
    """Exception raised for errors related to RTD client operations."""
    pass

class RTDConfigError(RTDError):
    """Exception raised for configuration-related errors."""
    pass

def handle_com_error(error_class: Type[RTDError] = RTDError):
    """
    Decorator to handle COM errors and convert them to appropriate RTD errors.
    Args:
        error_class: The specific RTDError subclass to raise. Defaults to RTDError.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except comtypes.COMError as e:
                hresult, text, details = e.args
                error_msg = f"COM error in {func.__name__}: [0x{hresult:08x}] {text}"
                logger.error(error_msg, exc_info=True)
                raise error_class(error_msg) from e
            except Exception as e:
                error_msg = f"Unexpected error in {func.__name__}: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise error_class(error_msg) from e
        return wrapper
    return decorator

def validate_connection_state(expected_states: List[RTDConnectionState]):
    """
    Decorator to validate the RTD connection state before executing a method.
    Args:
        expected_states: List of valid RTDConnectionState values for the method.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            current_state = getattr(self, '_state', RTDConnectionState.DISCONNECTED)
            if current_state not in expected_states:
                # Special case for heartbeat in disconnected state
                if func.__name__ == 'heartbeat' and current_state == RTDConnectionState.DISCONNECTED:
                    logger.debug(f"Skipping heartbeat in {current_state} state")
                    return None
                # Special case for Disconnect during or after shutdown
                if func.__name__ == 'Disconnect' and current_state in {
                    RTDConnectionState.DISCONNECTED,
                    RTDConnectionState.DISCONNECTING,
                }:
                    logger.debug(f"Skipping Disconnect in {current_state} state")
                    return None  # Silently return for repeated Disconnect calls
                # General case for disconnecting state
                if current_state == RTDConnectionState.DISCONNECTING:
                    logger.warning(f"Cannot call {func.__name__} during shutdown")
                    return None
                raise RTDConnectionError(
                    f"Invalid state for {func.__name__}: Expected {[s.name for s in expected_states]}, but was {current_state.name}"
                )
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def log_method_call(log_level: str = 'DEBUG'):
    """
    Decorator to log method entry and exit with optional timing.
    Args:
        log_level: The logging level to use. Defaults to 'DEBUG'.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            method_logger = getattr(self, 'logger', logger)
            log_func = getattr(method_logger, log_level.lower())
            
            arg_str = ', '.join([f"{arg}" for arg in args] + [f"{k}={v}" for k, v in kwargs.items()])
            log_func(f"Entering {func.__name__}({arg_str})")
            
            try:
                result = func(self, *args, **kwargs)
                log_func(f"Exiting {func.__name__}")
                return result
            except Exception as e:
                method_logger.error(f"Error in {func.__name__}: {str(e)}")
                raise
        return wrapper
    return decorator

def retry_on_error(max_retries: int = 3, delay: float = 1.0, 
                  allowed_exceptions: tuple = (RTDError,)):
    """
    Decorator to retry a function on specified exceptions.
    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
        allowed_exceptions: Tuple of exceptions that trigger retry
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except allowed_exceptions as e:
                    retries += 1
                    if retries == max_retries:
                        logger.error(f"Max retries ({max_retries}) reached for {func.__name__}")
                        raise
                    logger.warning(f"Retry {retries}/{max_retries} for {func.__name__} after error: {str(e)}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator