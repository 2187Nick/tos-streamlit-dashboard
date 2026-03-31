from datetime import date, timedelta
import numpy as np

class OptionSymbolBuilder:
    # Dictionary mapping futures to their exchanges
    FUTURES_EXCHANGES = {
        "/ZN": "XCBT",  # 10-Year T-Note
        "/ZB": "XCBT",  # 30-Year T-Bond
        "/ES": "XCME",  # E-mini S&P 500
        "/NQ": "XCME",  # E-mini NASDAQ
        "/RTY": "XCME", # E-mini Russell 2000
        "/YM": "XCBT",  # E-mini Dow
        "/CL": "XNYM",  # Crude Oil
        "/GC": "XCEC",  # Gold
        "/SI": "XCEC",  # Silver
        "/ZC": "XCBT",  # Corn
        "/ZS": "XCBT",  # Soybeans
        "/ZW": "XCBT",  # Wheat
    }

    # Dictionary mapping futures to their contract months
    FUTURES_MONTHS = {
        'F': '01',  # January
        'G': '02',  # February
        'H': '03',  # March
        'J': '04',  # April
        'K': '05',  # May
        'M': '06',  # June
        'N': '07',  # July
        'Q': '08',  # August
        'U': '09',  # September
        'V': '10',  # October
        'X': '11',  # November
        'Z': '12'   # December
    }

    # Dictionary mapping month numbers to futures codes
    MONTH_TO_CODE = {v: k for k, v in FUTURES_MONTHS.items()}

    # Dictionary mapping weekdays to codes for /ES options
    WEEKDAY_CODES = {
        0: "A",  # Monday
        1: "B",  # Tuesday
        2: "C",  # Wednesday
        3: "D",  # Thursday
        4: "W"   # Friday
    }

    @staticmethod
    def _round_to_nearest_strike(price: float, spacing: float) -> float:
        """Round price to nearest valid strike price based on strike spacing"""
        return round(price / spacing) * spacing

    @staticmethod
    def _is_third_friday(d: date) -> bool:
        """Check if date is the third Friday of its month"""
        # Find first day of the month
        first = date(d.year, d.month, 1)
        # Find first Friday
        friday = first + timedelta(days=((4 - first.weekday()) % 7))
        # Find third Friday
        third_friday = friday + timedelta(days=14)
        return d == third_friday

    @staticmethod
    def _is_third_week(d: date) -> bool:
        """Check if date is in the third week of its month"""
        return 15 <= d.day <= 21

    @staticmethod
    def _get_weekday_code(d: date) -> str:
        """Get the weekday code for /ES options"""
        return OptionSymbolBuilder.WEEKDAY_CODES.get(d.weekday(), "W")

    @staticmethod
    def _get_week_indicator(d: date) -> str:
        """
        Get the week indicator number (1-5) based on business week of the month
        First business week starts with the first trading day of the month
        """
        first_day = date(d.year, d.month, 1)
        target_day = d
        
        # Calculate the business week number
        if first_day.weekday() > 4:  # If first day is weekend
            # Adjust first_day to next Monday
            days_to_monday = (7 - first_day.weekday())
            first_day = first_day + timedelta(days=days_to_monday)
        
        days_difference = (target_day - first_day).days
        # Adjust for weekends
        weeks = (days_difference + first_day.weekday()) // 7 + 1
        
        # Handle edge case where the date is before first business day
        if target_day < first_day:
            return '1'
        
        #print(f"week: {str(min(max(weeks, 1), 5))}")
        
        # Ensure week number is between 1 and 5
        return str(min(max(weeks, 1), 5))

    @staticmethod
    def _get_futures_month_code(expiry: date) -> str:
        """Convert a date to a futures month code"""
        for code, month in OptionSymbolBuilder.FUTURES_MONTHS.items():
            if int(month) == expiry.month:
                return code
        return ''

    @staticmethod
    def _is_end_of_month(d: date) -> bool:
        """Check if date is the last trading day of the month"""
        next_day = d + timedelta(days=1)
        return next_day.month != d.month

    @staticmethod
    def _is_quarterly_expiration(d: date) -> bool:
        """Check if date is a quarterly expiration (3rd Friday of Mar, Jun, Sep, Dec)"""
        quarterly_months = {3, 6, 9, 12}  # March, June, September, December
        return d.month in quarterly_months and OptionSymbolBuilder._is_third_friday(d)
    
    @staticmethod
    def _get_zn_product_code(expiry: date) -> str:
        """
        Get the product code for /ZN options based on expiry date
        Special handling for quarterly expirations (3rd Friday of Mar, Jun, Sep, Dec):
        - AM settled: OZN[month_code][year] (e.g., OZNH25)
        
        Regular weekly format:
        - Mon: VY[week_indicator][month_code][year]
        - Wed: WY[week_indicator][month_code][year]
        - Friday: ZN[week_indicator][month_code][year]
        """
        month_code = OptionSymbolBuilder.MONTH_TO_CODE.get(f"{expiry.month:02d}")
        year = str(expiry.year)[-2:]
        
        # Check if it's end of month
        """ if OptionSymbolBuilder._is_end_of_month(expiry):
            return [f"QNE{month_code}{year}"] """
        
        # Get week indicator for non-EOM dates
        week_indicator = OptionSymbolBuilder._get_week_indicator(expiry)

        # Check if it's a quarterly expiration
        if OptionSymbolBuilder._is_quarterly_expiration(expiry):
            print(f"Detected quarterly expiration for {expiry}")
            return "OZN" + month_code + year,  # Not AM settled?
                  
        
        # Special handling for Friday (non-EOM)
        if expiry.weekday() == 0:  # Monday
            return [f"VY{week_indicator}{month_code}{year}"]
        elif expiry.weekday() == 2:  # Friday
            return [f"WY{week_indicator}{month_code}{year}"]
        elif expiry.weekday() == 4:  # Friday
            return [f"ZN{week_indicator}{month_code}{year}"]

    @staticmethod
    def _get_nq_product_code(expiry: date) -> str:
        """
        Get the product code for /NQ options based on expiry date
        Special handling for quarterly expirations (3rd Friday of Mar, Jun, Sep, Dec):
        - AM settled: NQ[month_code][year] (e.g., NQH25)
        
        Regular weekly format:
        - Mon-Thu: Q[week_indicator][weekday_code][month_code][year]
        - Friday: QN[week_indicator][month_code][year]
        - EOM: QNE[month_code][year]
        """
        month_code = OptionSymbolBuilder.MONTH_TO_CODE.get(f"{expiry.month:02d}")
        year = str(expiry.year)[-2:]
        
        # Check if it's end of month
        if OptionSymbolBuilder._is_end_of_month(expiry):
            return [f"QNE{month_code}{year}"]
        
        # Get week indicator for non-EOM dates
        week_indicator = OptionSymbolBuilder._get_week_indicator(expiry)

        # Check if it's a quarterly expiration
        if OptionSymbolBuilder._is_quarterly_expiration(expiry):
            print(f"Detected quarterly expiration for {expiry}")
            return ["NQ" + month_code + year,  # AM settled format
                   f"QN + {week_indicator}{month_code}{year}"]   # Regular settled format
        
        # Special handling for Friday (non-EOM)
        if expiry.weekday() == 4:  # Friday
            return [f"QN{week_indicator}{month_code}{year}"]
        else:
            # Monday through Thursday
            weekday_code = OptionSymbolBuilder._get_weekday_code(expiry)
            return [f"Q{week_indicator}{weekday_code}{month_code}{year}"]

    @staticmethod
    def _get_es_product_code(expiry: date) -> str:
        """
        Get the product code for /ES options based on expiry date
        Special handling for quarterly expirations (3rd Friday of Mar, Jun, Sep, Dec):
        - AM settled: ES[quarter_code][year] (e.g., ESH25)
        - Regular settled: E[weekday_code][month_code][year] (e.g., EWH25)
        
        Regular weekly format:
        - Mon-Thu: E[week_indicator][weekday_code][month_code][year]
        - Friday: E[weekday_code][week_indicator][month_code][year]
        - EOM: EW[month_code][year]
        """
        month_code = OptionSymbolBuilder.MONTH_TO_CODE.get(f"{expiry.month:02d}")
        year = str(expiry.year)[-2:]
        
        # Check if it's a quarterly expiration
        if OptionSymbolBuilder._is_quarterly_expiration(expiry):
            print(f"Detected quarterly expiration for {expiry}")
            return ["ES" + month_code + year,  # AM settled format
                   "EW" + month_code + year]   # Regular settled format
        
        # Regular formatting for non-quarterly dates
        weekday_code = OptionSymbolBuilder._get_weekday_code(expiry)
        
        # Check if it's end of month
        if OptionSymbolBuilder._is_end_of_month(expiry):
            return [f"EW{month_code}{year}"]
        
        # Get week indicator for non-EOM dates
        week_indicator = OptionSymbolBuilder._get_week_indicator(expiry)
        
        # Special handling for Friday (non-EOM)
        if expiry.weekday() == 4:  # Friday
            return [f"E{weekday_code}{week_indicator}{month_code}{year}"]
        else:
            return [f"E{week_indicator}{weekday_code}{month_code}{year}"]

    @staticmethod
    def _format_strike(strike: float, is_futures: bool = False, strike_spacing: float = None) -> str:
        """
        Format strike price string for options
        
        Args:
            strike: Strike price to format
            is_futures: Whether this is a futures option
            strike_spacing: The spacing between strikes (e.g., 0.25, 0.5, 2.5)
        
        Returns:
            Formatted strike price string
        
        Examples:
            109.25 -> "109.25" (for quarter points)
            109.50 -> "109.5" (for half points)
            109.75 -> "109.75" (for quarter points)
            100.00 -> "100" (for whole numbers)
        """
        # Handle quarter point strikes
        if strike_spacing == 0.25:
            if abs(strike % 0.25) < 0.001:  # Handle floating point comparison
                if strike % 1 == 0:  # Whole number
                    return f"{int(strike)}"
                # For half points, use .1f
                if abs((strike % 1) - 0.5) < 0.001:
                    return f"{strike:.1f}"
                # For quarter points, use .2f
                return f"{strike:.2f}"
        
        # Handle half point strikes
        if strike_spacing in [0.5, 2.5]:
            if abs(strike % 1 - 0.5) < 0.001:  # Handle floating point comparison
                return f"{strike:.1f}"
        
        # Default to whole number for other cases
        return f"{int(round(strike))}"

    @staticmethod
    def build_symbols(base_symbol: str, expiry: date, current_price: float, strike_range: int, strike_spacing: float) -> list:
        """
        Builds a list of option symbols for both calls and puts
        """
        if not current_price or current_price <= 0:
            print("Invalid current price")
            return []
            
        if not strike_range or strike_range <= 0:
            print("Invalid strike range")
            return []
            
        if not strike_spacing or strike_spacing <= 0:
            print("Invalid strike spacing")
            return []
            
        # Get exchange suffix for futures
        exchange = OptionSymbolBuilder.FUTURES_EXCHANGES.get(base_symbol, "XCBT")
            
        # Round current price to nearest valid strike
        rounded_price = OptionSymbolBuilder._round_to_nearest_strike(current_price, strike_spacing)
        print(f"Rounded price: {rounded_price}, Range: ±{strike_range}, Spacing: {strike_spacing}")
        
        # Generate strike prices using numpy arange
        num_strikes = int(2 * strike_range / strike_spacing) + 1
        strikes = np.linspace(
            rounded_price - strike_range,
            rounded_price + strike_range,
            num_strikes
        )
        
        if len(strikes) == 0:
            print("No strikes generated")
            return []
            
        print(f"Generated {len(strikes)} strikes from {strikes[0]} to {strikes[-1]}")
        
        symbols = []
        
        # Special handling for /ES futures options
        """
        Need to check GEX math on /ES and /NQ. Do we divide it by 2?
        """
        if base_symbol == "/ES":
            product_codes = OptionSymbolBuilder._get_es_product_code(expiry)
            for product_code in product_codes:  
                for strike in strikes:
                    strike_str = OptionSymbolBuilder._format_strike(strike, is_futures=True)
                    # For Quarterly settlement, How do we display the pm settled options?
                    call_symbol = f"./{product_code}C{strike_str}:{exchange}"
                    put_symbol = f"./{product_code}P{strike_str}:{exchange}"
                    symbols.extend([call_symbol, put_symbol])

        
        # Special handling for /NQ futures options
        elif base_symbol == "/NQ":
            product_codes = OptionSymbolBuilder._get_nq_product_code(expiry)
            for product_code in product_codes:  
                for strike in strikes:
                    strike_str = OptionSymbolBuilder._format_strike(strike, is_futures=True)
                    # For Quarterly settlement, How do we display the pm settled options?
             
                    call_symbol = f"./{product_code}C{strike_str}:{exchange}"
                    put_symbol = f"./{product_code}P{strike_str}:{exchange}"
                    symbols.extend([call_symbol, put_symbol])

        # In the build_symbols method, modify the /ZN section:

            """
            The contract rolls over at a different time than NQ and ES
            Once we have that calc done. Then should be close on the /ZN options
            """
        elif base_symbol == "/ZN":
            product_codes = OptionSymbolBuilder._get_zn_product_code(expiry)
            for product_code in product_codes:  
                for strike in strikes:
                    strike_str = OptionSymbolBuilder._format_strike(
                        strike, 
                        is_futures=True,
                        strike_spacing=strike_spacing
                    )
                    call_symbol = f"./{product_code}C{strike_str}:{exchange}"
                    put_symbol = f"./{product_code}P{strike_str}:{exchange}"
                    symbols.extend([call_symbol, put_symbol])
                
        # Handle other futures options
        elif base_symbol.startswith('/'):
            month_code = OptionSymbolBuilder._get_futures_month_code(expiry)
            futures_base = f"{base_symbol[1:]}1{month_code}{str(expiry.year)[-2:]}"
            for strike in strikes:
                strike_str = OptionSymbolBuilder._format_strike(strike, is_futures=True)
                call_symbol = f"./{futures_base}C{strike_str}:{exchange}"
                put_symbol = f"./{futures_base}P{strike_str}:{exchange}"
                symbols.extend([call_symbol, put_symbol])
                
        # Handle equity/index options
        else:
            if not OptionSymbolBuilder._is_third_friday(expiry):
                if base_symbol == "SPX":
                    base_symbol = "SPXW"
                elif base_symbol == "NDX":
                    base_symbol = "NDXP"
                elif base_symbol == "RUT":
                    base_symbol = "RUTW"
            
            date_str = expiry.strftime("%y%m%d")
            for strike in strikes:
                strike_str = OptionSymbolBuilder._format_strike(strike)
                call_symbol = f".{base_symbol}{date_str}C{strike_str}"
                put_symbol = f".{base_symbol}{date_str}P{strike_str}"
                symbols.extend([call_symbol, put_symbol])
        
        if not symbols:
            print("No symbols generated")
            return []
            
        print(f"Generated {len(symbols)} total symbols. First few: {symbols[:4]}")
        return symbols
