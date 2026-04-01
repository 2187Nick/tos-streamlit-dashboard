#  app.py
import time
import threading
from queue import Queue
import streamlit as st
from src.rtd.rtd_worker import RTDWorker
from src.utils.option_symbol_builder import OptionSymbolBuilder
from src.ui.gamma_chart import GammaChartBuilder
from src.ui.dashboard_layout import DashboardLayout


def _print_generated_symbols(base_symbol: str, expiry_date, price: float, option_symbols: list) -> None:
    """Print generated symbols to the Streamlit terminal for manual verification."""
    if not option_symbols:
        print(f"No option symbols generated for {base_symbol}")
        return

    print("\n" + "=" * 80)
    print(f"Generated option symbols for {base_symbol}")
    print(f"Expiry: {expiry_date} | Price used: {price} | Count: {len(option_symbols)}")
    print("-" * 80)

    for index, option_symbol in enumerate(option_symbols, start=1):
        print(f"{index:03d}: {option_symbol}")

    print("=" * 80 + "\n")


def _extract_strike_from_option_symbol(option_symbol: str):
    """Extract the numeric strike from an option symbol."""
    symbol_without_exchange = option_symbol.split(':', 1)[0]
    option_marker_index = max(
        symbol_without_exchange.rfind('C'),
        symbol_without_exchange.rfind('P')
    )

    if option_marker_index == -1:
        raise ValueError(f"No call/put marker found in symbol: {option_symbol}")

    strike_part = symbol_without_exchange[option_marker_index + 1:]
    print(f"Extracted strike part from option symbol: {strike_part}")

    strike = float(strike_part)
    return int(strike) if strike.is_integer() else strike

# Initialize session state
if 'initialized' not in st.session_state:
    print("Initializing")
    st.session_state.initialized = False
    st.session_state.data_queue = Queue()
    st.session_state.stop_event = threading.Event()
    st.session_state.current_price = None
    st.session_state.option_symbols = []
    st.session_state.active_thread = None
    st.session_state.last_figure = None
    st.session_state.loading_complete = False
    st.session_state.last_chart_type = None  # Track last chart type
    st.session_state.last_graph_type = None  # Track last graph type

# Setup UI
pos_color, neg_color, graph_type, chart_orientation = DashboardLayout.setup_page()
symbol, expiry_date, strike_range, strike_spacing, refresh_rate, chart_type, start_stop_button = DashboardLayout.create_input_section()

# Check if chart type changed
if 'last_chart_type' in st.session_state and st.session_state.last_chart_type != chart_type:
    st.session_state.last_figure = None  # Force chart update

# Update last chart type
st.session_state.last_chart_type = chart_type

# Create placeholder for chart
gamma_chart = st.empty()

# Initialize chart if needed
if 'chart_builder' not in st.session_state:
    st.session_state.chart_builder = GammaChartBuilder(symbol)
    st.session_state.last_figure = st.session_state.chart_builder.create_empty_chart()

# Update chart colors
st.session_state.chart_builder.set_colors(pos_color, neg_color)

if st.session_state.last_figure:
    gamma_chart.plotly_chart(st.session_state.last_figure, use_container_width=True, key="main_chart")

# Handle start/stop button clicks
if start_stop_button:
    if not st.session_state.initialized:
        # Clean stop any existing thread
        if st.session_state.active_thread:
            st.session_state.stop_event.set()
            st.session_state.active_thread.join(timeout=2.0)  # Increased timeout
        
        # Reset state
        st.session_state.stop_event = threading.Event()
        st.session_state.data_queue = Queue()
        st.session_state.rtd_worker = RTDWorker(st.session_state.data_queue, st.session_state.stop_event)
        st.session_state.option_symbols = []  # Reset option symbols
        
        # Only reset chart if symbol changed
        if 'last_symbol' not in st.session_state or st.session_state.last_symbol != symbol:
            st.session_state.chart_builder = GammaChartBuilder(symbol)
            st.session_state.last_figure = st.session_state.chart_builder.create_empty_chart()
            gamma_chart.plotly_chart(st.session_state.last_figure, use_container_width=True, key="reset_chart")
            st.session_state.last_symbol = symbol
        
        # Start with stock symbol only to get price first
        try:
            thread = threading.Thread(
                target=st.session_state.rtd_worker.start,
                args=([symbol],),
                daemon=True
            )
            thread.start()
            st.session_state.active_thread = thread
            st.session_state.initialized = True
            time.sleep(0.1)  # Brief pause for connection setup
            st.rerun()
        except Exception as e:
            st.error(f"Failed to start RTD worker: {str(e)}")
            st.session_state.initialized = False
    else:
        # Stop tracking but keep the chart
        st.session_state.stop_event.set()
        if st.session_state.active_thread:
            st.session_state.active_thread.join(timeout=1.0)  # Increased timeout
        st.session_state.active_thread = None
        st.session_state.initialized = False
        st.session_state.loading_complete = False
        st.session_state.option_symbols = []  # Reset option symbols
        #time.sleep(1)  # Add delay before allowing restart
        st.rerun()

# Display updates
if st.session_state.initialized:
    try:
        if not st.session_state.data_queue.empty():
            data = st.session_state.data_queue.get()
            
            if "error" in data:
                st.error(data["error"])
            elif "status" not in data:
                # For futures symbols, append exchange suffix for price lookup
                if symbol.startswith('/'):
                    exchange = OptionSymbolBuilder.FUTURES_EXCHANGES.get(symbol, "XCBT")
                    print(f"Extracted exchange for futures: {exchange}")  # Debug logging
                    price_key = f"{symbol}:{exchange}:LAST"
                    print(f"Initial futures price lookup - Key: {price_key}")  # Debug logging
                else:
                    price_key = f"{symbol}:LAST"
                
                price = data.get(price_key)
                print(f"Initial price data received: {price} for {price_key}")  # Debug logging
                
                if price:
                    print(f"Building option chain for {symbol} at price: {price}")  # Debug logging
                    # If we just got the price and don't have option symbols yet,
                    # restart with all symbols
                    if not st.session_state.option_symbols:
                        option_symbols = OptionSymbolBuilder.build_symbols(
                            symbol, expiry_date, price, strike_range, strike_spacing
                        )
                        if symbol.startswith('/'):
                            _print_generated_symbols(symbol, expiry_date, price, option_symbols)
                        
                        # Stop current thread
                        st.session_state.stop_event.set()
                        if st.session_state.active_thread:
                            st.session_state.active_thread.join(timeout=1.0)
                        
                        # Start new thread with all symbols
                        st.session_state.stop_event = threading.Event()
                        st.session_state.option_symbols = option_symbols
                        all_symbols = [f"{symbol}:{exchange}" if symbol.startswith('/') else symbol] + option_symbols
                        print(f"Subscribing to base symbol: {all_symbols[0]}")  # Debug logging
                        
                        # Create new RTD worker and thread
                        st.session_state.rtd_worker = RTDWorker(st.session_state.data_queue, st.session_state.stop_event)
                        thread = threading.Thread(
                            target=st.session_state.rtd_worker.start,
                            args=(all_symbols,),
                            daemon=True
                        )
                        thread.start()
                        st.session_state.active_thread = thread
                        time.sleep(0.1)
                
                # Update chart
                # Update chart
                if st.session_state.option_symbols:
                    strikes = []
                    for sym in st.session_state.option_symbols:
                        try:
                            if sym.startswith('./'):  # Futures option symbol
                                strikes.append(_extract_strike_from_option_symbol(sym))
                            else:  # Stock option symbol
                                strikes.append(_extract_strike_from_option_symbol(sym))
                                
                        except (ValueError, IndexError) as e:
                            print(f"Error extracting strike from {sym}: {e}")
                            continue
                    
                    if strikes:
                        strikes = sorted(set(strikes))
                        print(f"Extracted strikes: {strikes[:5]}...")  # Debug log first 5 strikes
                        
                        # Always update chart if type changed or we don't have a figure
                        if (st.session_state.last_figure is None or 
                            ('last_chart_type' in st.session_state and st.session_state.last_chart_type != chart_type) or
                            ('last_graph_type' not in st.session_state or st.session_state.last_graph_type != graph_type)):
                            force_update = True
                        else:
                            force_update = False

                        # Convert chart_orientation to vertical boolean
                        vertical = (chart_orientation == "Vertical")

                        display_type = "Gamma Exposure" if chart_type == "GEX" else chart_type

                        # Check if we have any valid data before creating chart
                        if data:
                            fig = st.session_state.chart_builder.create_chart(
                                data, strikes, st.session_state.option_symbols, 
                                display_type, graph_type, chart_orientation
                            )
                            st.session_state.last_figure = fig
                            gamma_chart.plotly_chart(fig, use_container_width=True, key=f"update_chart_{chart_type}_{graph_type}")
                        else:
                            print("No data available for chart update")
                    else:
                        print("No valid strikes extracted from symbols")
                        force_update = False

                    if not st.session_state.loading_complete:
                        st.session_state.loading_complete = True
                    elif not force_update:  # Only sleep if not forced update
                        time.sleep(refresh_rate)
                    st.session_state.last_chart_type = chart_type
                    st.session_state.last_graph_type = graph_type  # Store last graph type
                    if st.session_state.initialized:
                        st.rerun()
        else:
            if st.session_state.initialized:
                # Poll faster before first data loads, slower after
                wait = 0.1 if not st.session_state.loading_complete else 0.5
                time.sleep(wait)
                st.rerun()
                
    except Exception as e:
        st.error(f"Display Error: {str(e)}")
        print(f"Error details: {e}")