import plotly.graph_objects as go
from src.utils.option_symbol_builder import OptionSymbolBuilder

class GammaChartBuilder:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.pos_color = '#00FF00'  # Default green
        self.neg_color = '#FF0000'  # Default red

    def set_colors(self, pos_color: str, neg_color: str):
        """Set custom colors for the chart"""
        self.pos_color = pos_color
        self.neg_color = neg_color

    def create_empty_chart(self) -> go.Figure:
        """Create initial empty chart"""
        fig = go.Figure()
        self._set_layout(fig, 1, None)  # Use 1 as default range, no price
        return fig

    def create_chart(self, data: dict, strikes: list, option_symbols: list, chart_type: str = "GEX", graph_type: str = "Bar", chart_orientation: str = "Horizontal") -> go.Figure:
        """Build and return the chart"""
        fig = go.Figure()
        
        if not strikes or not option_symbols:
            print("No strikes or option symbols available")
            return self.create_empty_chart()
        
        # Get current price first
        if self.symbol.startswith('/'):
            exchange = OptionSymbolBuilder.FUTURES_EXCHANGES.get(self.symbol, "XCBT")
            price_key = f"{self.symbol}:{exchange}:LAST"
            current_price = float(data.get(price_key, 0))
            print(f"Futures price lookup key: {price_key}")
            print(f"Current futures price: {current_price}")
        else:
            current_price = float(data.get(f"{self.symbol}:LAST", 0))
            
        if current_price == 0:
            print("No price data available")
            return self.create_empty_chart()

        # Get appropriate values based on chart type
        vertical = chart_orientation == "Vertical"
        
        # Get appropriate values based on chart type
        if chart_type in ["GEX", "Gamma Exposure"]:
            pos_values, neg_values = self._calculate_gex_values(data, strikes, option_symbols)
            values_label = "Gamma Exposure ($ per 1% move)"
            if pos_values or neg_values:  # Only scale if we have values
                pos_values = [x/1000000 for x in pos_values]
                neg_values = [x/1000000 for x in neg_values]
        elif chart_type == "Volume":
            pos_values, neg_values = self._calculate_volume_values(data, strikes, option_symbols)
            values_label = "Volume"
        else:  # Open Interest
            pos_values, neg_values = self._calculate_oi_values(data, strikes, option_symbols)
            values_label = "Open Interest"

        if not pos_values and not neg_values:
            print(f"No {chart_type} data available")
            return self.create_empty_chart()

        # Round the values
        pos_values = [round(x, 0) for x in pos_values]
        neg_values = [round(x, 0) for x in neg_values]

        # Find max values and their strikes with safety checks
        max_pos_idx = pos_values.index(max(pos_values)) if any(pos_values) else -1
        max_neg_idx = neg_values.index(min(neg_values)) if any(neg_values) else -1
        
        max_pos_strike = strikes[max_pos_idx] if max_pos_idx >= 0 and max_pos_idx < len(strikes) else None
        max_neg_strike = strikes[max_neg_idx] if max_neg_idx >= 0 and max_neg_idx < len(strikes) else None
        
        # Fixed max value calculation with safety checks
        max_pos = max(pos_values) if pos_values else 0
        min_neg = min(neg_values) if neg_values else 0
        max_abs_value = max(abs(min_neg), abs(max_pos))
        
        if max_abs_value == 0:
            print("No non-zero values to display")
            max_abs_value = 1
            
        padding = max_abs_value * 0.3
        chart_range = max_abs_value + padding

        self._add_traces(fig, pos_values, neg_values, strikes, vertical, chart_type, graph_type)
        
        # Add price line
        if vertical:
            # Find the index where current price would fit in strikes
            price_index = 0
            for i, strike in enumerate(strikes):
                if float(strike) > current_price:
                    price_index = i - 0.5
                    break
                elif float(strike) == current_price:
                    price_index = i
                    break
                price_index = i + 0.5

            #print(f"Price index: {price_index}")
            
            # Add vertical line at the correct position
            fig.add_vline(
                x=price_index,
                line_color="blue",
                line_width=1,
                annotation_text=f"${current_price:.2f}",
                annotation_position="top"
            )
        else:
            fig.add_hline(
                y=current_price,
                line_color="blue",
                line_width=2,
                annotation_text=f"${current_price:.2f}",
                annotation_position="top left"
            )

        self._add_annotations(
            fig, max_pos, min_neg, padding,
            max_pos_idx, max_pos_strike, max_neg_idx, max_neg_strike,
            vertical, chart_type
        )

        self._set_layout(fig, chart_range, current_price, vertical, values_label, strikes, graph_type)
        
        return fig

    def _find_option_symbol(self, option_symbols: list, strike: str, option_type: str) -> str:
        """
        Find option symbol for given strike price while handling exchange suffixes
        
        Args:
            option_symbols: List of option symbols
            strike: Strike price (can be int or float)
            option_type: 'C' for calls or 'P' for puts
        
        Returns:
            Matching option symbol
        """
        strike_value = int(float(strike)) if float(strike).is_integer() else float(strike)
        strike_str = str(strike_value)
        print(f"Looking for {option_type}{strike_str} in options")  # Debug logging
        
        try:
            for sym in option_symbols:
                parsed_option_type, parsed_strike = self._extract_option_type_and_strike(sym)
                if parsed_option_type == option_type and parsed_strike == strike_value:
                    return sym
            
            print(f"Available symbols: {option_symbols[:2]}...")  # Show first few symbols
            raise ValueError(f"No matching symbol found for {option_type}{strike_str}")
            
        except Exception as e:
            print(f"Error finding symbol for {option_type}{strike_str}: {e}")
            raise

    def _extract_option_type_and_strike(self, option_symbol: str):
        """Parse an option symbol and return its option type and numeric strike."""
        symbol_without_exchange = option_symbol.split(':', 1)[0]
        call_index = symbol_without_exchange.rfind('C')
        put_index = symbol_without_exchange.rfind('P')
        option_marker_index = max(call_index, put_index)

        if option_marker_index == -1:
            raise ValueError(f"No call/put marker found in symbol: {option_symbol}")

        option_type = symbol_without_exchange[option_marker_index]
        strike_part = symbol_without_exchange[option_marker_index + 1:]
        strike = float(strike_part)
        parsed_strike = int(strike) if strike.is_integer() else strike
        return option_type, parsed_strike

    def _calculate_gex_values(self, data, strikes, option_symbols):
        pos_gex_values = []
        neg_gex_values = []
        
        try:
            # Handle futures price lookup with exchange suffix
            if self.symbol.startswith('/'):
                exchange = OptionSymbolBuilder.FUTURES_EXCHANGES.get(self.symbol, "XCBT")
                price_key = f"{self.symbol}:{exchange}:LAST"
                underlying_price = float(data.get(price_key, 0))
                #print(f"GEX calculation - Futures price key: {price_key}")
                #print(f"GEX calculation - Futures price: {underlying_price}")
            else:
                underlying_price = float(data.get(f"{self.symbol}:LAST", 0))
            
        except (ValueError, TypeError):
            underlying_price = 0
            
        if underlying_price == 0:
            print("Warning: Underlying price is 0")
            return [], []
        
        for strike in strikes:
            try:
                call_symbol = self._find_option_symbol(option_symbols, strike, 'C')
                put_symbol = self._find_option_symbol(option_symbols, strike, 'P')
                
                #print(f"Processing strike {strike}")
                #print(f"Call symbol: {call_symbol}")
                #print(f"Put symbol: {put_symbol}")
                
                try:
                    call_gamma = float(data.get(f"{call_symbol}:GAMMA", 0))
                    call_oi = float(data.get(f"{call_symbol}:OPEN_INT", 0))
                except (ValueError, TypeError):
                    print(f"Warning: Invalid gamma/oi for {call_symbol}")
                    call_gamma = 0
                    call_oi = 0
                    
                try:
                    put_gamma = float(data.get(f"{put_symbol}:GAMMA", 0))
                    put_oi = float(data.get(f"{put_symbol}:OPEN_INT", 0))
                except (ValueError, TypeError):
                    print(f"Warning: Invalid gamma/oi for {put_symbol}")
                    put_gamma = 0
                    put_oi = 0
                
                # gamma exposure per 1% change in the underlying price
                gex = ((call_oi*call_gamma) - (put_oi*put_gamma)) * 100 * (underlying_price*underlying_price) * .01
                #print(f"GEX for strike {strike}: {gex}")

            except Exception as e:
                print(f"Error processing strike {strike}: {str(e)}")
                gex = 0
            
            if gex > 0:
                pos_gex_values.append(gex)
                neg_gex_values.append(0)
            else:
                pos_gex_values.append(0)
                neg_gex_values.append(gex)  # Keep negative
        
        return pos_gex_values, neg_gex_values

    def _calculate_oi_values(self, data, strikes, option_symbols):
        call_values = []
        put_values = []
        for strike in strikes:
            try:
                call_symbol = self._find_option_symbol(option_symbols, strike, 'C')
                put_symbol = self._find_option_symbol(option_symbols, strike, 'P')
                
                call_oi = float(data.get(f"{call_symbol}:OPEN_INT", 0))
                put_oi = float(data.get(f"{put_symbol}:OPEN_INT", 0))
                
                call_values.append(call_oi)
                put_values.append(-put_oi)  # Keep negative
            except Exception as e:
                print(f"Error processing OI for strike {strike}: {e}")
                call_values.append(0)
                put_values.append(0)
        return call_values, put_values

    def _calculate_volume_values(self, data, strikes, option_symbols):
        call_values = []
        put_values = []
        for strike in strikes:
            try:
                call_symbol = self._find_option_symbol(option_symbols, strike, 'C')
                put_symbol = self._find_option_symbol(option_symbols, strike, 'P')
                
                call_volume = float(data.get(f"{call_symbol}:VOLUME", 0))
                put_volume = float(data.get(f"{put_symbol}:VOLUME", 0))
                
                call_values.append(call_volume)
                put_values.append(-put_volume)  # Keep negative
            except Exception as e:
                print(f"Error processing volume for strike {strike}: {e}")
                call_values.append(0)
                put_values.append(0)
        return call_values, put_values

    def _add_traces(self, fig, pos_values, neg_values, strikes, vertical=False, chart_type="GEX", graph_type="Bar"):
        # Determine trace names based on chart type
        if chart_type in ["GEX", "Gamma Exposure"]:
            pos_name = "Positive GEX"
            neg_name = "Negative GEX"
        else:
            pos_name = "Calls"
            neg_name = "Puts"

        # Convert strikes to strings for categorical axis
        strike_labels = [str(strike) for strike in strikes]
        
        # Safely calculate max values with empty list handling
        pos_max = max(pos_values) if pos_values else 0
        neg_max = max(abs(val) for val in neg_values) if neg_values else 0
        max_abs_value = max(pos_max, neg_max)
        
        # Scale factor for bubble size based on max absolute value
        bubble_scale = 50 / max_abs_value if max_abs_value > 0 else 1
        
        # Define trace type and additional properties based on graph_type
        trace_props = {
            "Bar": {"type": go.Bar, "extra": {}},
            "Line": {"type": go.Scatter, "extra": {"mode": "lines", "line_shape": "linear"}},
            "Scatter": {"type": go.Scatter, "extra": {"mode": "markers"}},
            "Area": {"type": go.Scatter, "extra": {"mode": "lines", "fill": "tonexty", "stackgroup": "one"}},
            "Step": {"type": go.Scatter, "extra": {"mode": "lines", "line_shape": "hv"}},
            "Bubble": {"type": go.Scatter, "extra": {
                "mode": "markers",
                "marker": {
                    "sizemode": "area",
                    "showscale": True,
                    "colorscale": [[0, "red"], [0.5, "white"], [1.0, "green"]]
                }
            }}
        }
        
        trace_config = trace_props.get(graph_type, trace_props["Bar"])
        TraceType = trace_config["type"]
        extra_props = trace_config["extra"].copy()  # Make a copy to modify for each trace
        
        if vertical:
            common_props = {
                "x": strike_labels,
                "showlegend": True,
            }
            
            # Special handling for bubble chart
            if graph_type == "Bubble":
                # Combine positive and negative values into a single trace
                all_values = [p if p != 0 else n for p, n in zip(pos_values, neg_values)]
                sizes = [abs(val) * bubble_scale for val in all_values]
                colors = all_values  # Use values for colors
                
                extra_props["marker"].update({
                    "size": sizes,
                    "color": colors,
                    "sizeref": 2 * max(sizes) / (40**2),  # Normalize bubble sizes
                })
                
                fig.add_trace(TraceType(
                    y=all_values,
                    name="GEX",
                    **common_props,
                    **extra_props
                ))
            else:
                # Add positive values trace
                fig.add_trace(TraceType(
                    y=pos_values,
                    name=pos_name,
                    marker_color=self.pos_color,
                    **common_props,
                    **extra_props
                ))
                
                # Add negative values trace
                fig.add_trace(TraceType(
                    y=neg_values,
                    name=neg_name,
                    marker_color=self.neg_color,
                    **common_props,
                    **extra_props
                ))
        else:
            common_props = {
                "y": strikes,
                "showlegend": True,
            }
            
            # For horizontal orientation
            orientation_props = {"orientation": "h"} if graph_type == "Bar" else {}
            
            # Special handling for bubble chart in horizontal mode
            if graph_type == "Bubble":
                # Combine positive and negative values into a single trace
                all_values = [p if p != 0 else n for p, n in zip(pos_values, neg_values)]
                sizes = [abs(val) * bubble_scale for val in all_values]
                colors = all_values  # Use values for colors
                
                extra_props["marker"].update({
                    "size": sizes,
                    "color": colors,
                    "sizeref": 2 * max(sizes) / (40**2),  # Normalize bubble sizes
                })
                
                fig.add_trace(TraceType(
                    x=all_values,
                    name="GEX",
                    **common_props,
                    **extra_props
                ))
            else:
                # Add positive values trace
                fig.add_trace(TraceType(
                    x=pos_values,
                    name=pos_name,
                    marker_color=self.pos_color,
                    **common_props,
                    **orientation_props,
                    **extra_props
                ))
                
                # Add negative values trace
                fig.add_trace(TraceType(
                    x=neg_values,
                    name=neg_name,
                    marker_color=self.neg_color,
                    **common_props,
                    **orientation_props,
                    **extra_props
                ))

        # Special handling for Area charts to ensure proper stacking
        if graph_type == "Area":
            fig.update_layout(hovermode="x unified")

    def _add_annotations(self, fig, max_pos, min_neg, padding, max_pos_idx, max_pos_strike, max_neg_idx, max_neg_strike, vertical=False, chart_type="GEX"):
        if max_pos == 0 and min_neg == 0:
            # No data to annotate
            return

        annotation_offset = padding * 0.7
        
        # Determine text format based on chart type
        is_gex = chart_type in ["GEX", "Gamma Exposure"]
        
        if vertical:
            if max_pos_idx >= 0 and max_pos > 0:
                text = f"+${round(max_pos)}M" if is_gex else f"+{round(max_pos):,}"
                fig.add_annotation(
                    x=max_pos_idx,  # Use index position for x
                    y=max_pos + (padding * 0.2),  # Add small padding above bar
                    text=text,
                    showarrow=True,
                    arrowhead=2,
                    ay=-20,
                    ax=0,
                    align="center",
                    yshift=10
                )
            
            if max_neg_idx >= 0 and min_neg < 0:
                text = f"-${abs(round(min_neg))}M" if is_gex else f"-{abs(round(min_neg)):,}"
                fig.add_annotation(
                    x=max_neg_idx,  # Use index position for x
                    y=min_neg - (padding * 0.2),  # Add small padding below bar
                    text=text,
                    showarrow=True,
                    arrowhead=2,
                    ay=20,
                    ax=0,
                    align="center",
                    yshift=-10
                )

            # Add volume annotations for vertical mode
            if chart_type == "Volume":
                if max_pos_idx >= 0 and max_pos > 0:
                    fig.add_annotation(
                        x=max_pos_idx,
                        y=max_pos + (padding * 0.3),
                        text="Top Volume",
                        showarrow=True,
                        arrowhead=2,
                        ay=-40,
                        ax=0,
                        align="center"
                    )
                if max_neg_idx >= 0 and min_neg < 0:
                    fig.add_annotation(
                        x=max_neg_idx,
                        y=min_neg - (padding * 0.3),
                        text="Top Volume",
                        showarrow=True,
                        arrowhead=2,
                        ay=40,
                        ax=0,
                        align="center"
                    )
        else:
            if max_pos_idx >= 0 and max_pos > 0:
                text = f"+${round(max_pos)}M" if is_gex else f"+{round(max_pos):,}"
                fig.add_annotation(
                    x=max_pos,
                    y=max_pos_strike,
                    text=text,
                    showarrow=True,
                    arrowhead=2,
                    ax=min(40, annotation_offset * 30),
                    ay=0,
                    align="left"
                )
            
            if max_neg_idx >= 0 and min_neg < 0:
                text = f"-${abs(round(min_neg))}M" if is_gex else f"-{abs(round(min_neg)):,}"
                fig.add_annotation(
                    x=min_neg,
                    y=max_neg_strike,
                    text=text,
                    showarrow=True,
                    arrowhead=2,
                    ax=max(-40, -annotation_offset * 30),
                    ay=0,
                    align="right"
                )

            # Horizontal mode volume annotations
            if chart_type == "Volume":
                if max_pos_idx >= 0 and max_pos > 0:
                    fig.add_annotation(
                        x=max_pos,
                        y=max_pos_strike,
                        text="Top Volume",
                        showarrow=True,
                        arrowhead=2,
                        ax=annotation_offset * 30,
                        ay=0,
                        align="left"
                    )
                if max_neg_idx >= 0 and min_neg < 0:
                    fig.add_annotation(
                        x=min_neg,
                        y=max_neg_strike,
                        text="Top Volume",
                        showarrow=True,
                        arrowhead=2,
                        ax=-annotation_offset * 30,
                        ay=0,
                        align="right"
                    )

    def _set_layout(self, fig, chart_range, current_price=None, vertical=False, values_label="Gamma Exposure ($M)", strikes=None, graph_type="Bar"):
        price_str = f" Price: ${current_price:.2f}" if current_price else ""
        layout_args = {
            'title': f'{self.symbol} {values_label}   {price_str}',
            'barmode': 'relative',  # Use relative mode for both orientations
            'showlegend': True,
            'legend': dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            'height': 600
        }

        if vertical:
            # Convert strikes to strings for categorical axis
            strike_labels = [str(x) for x in strikes] if strikes else []
            
            layout_args.update({
                'xaxis_title': 'Strike Price',
                'yaxis_title': values_label,
                'yaxis': dict(
                    range=[-chart_range, chart_range],
                    zeroline=True,
                    zerolinewidth=1,
                    zerolinecolor='black',
                ),
                'xaxis': dict(
                    tickmode='array',
                    ticktext=strike_labels,
                    tickvals=strike_labels,
                    tickangle=45,
                    type='category',
                    # Force domain to be full width and constrain price line
                    domain=[0, 1],
                    # Ensure bars are spaced properly
                    rangeslider=dict(visible=False),
                    automargin=True
                ),
            })
            
            # Add bargap for better spacing in vertical mode
            if graph_type != "Bubble":  # Don't add bargap for bubble charts
                layout_args['bargap'] = 0.15
                
            # Special handling for bubble charts
            if graph_type == "Bubble":
                layout_args.update({
                    'hoverlabel': dict(
                        bgcolor="white",
                        font_size=12,
                        font_family="Arial"
                    ),
                    'hovermode': 'closest'
                })
                
        else:
            layout_args.update({
                'xaxis_title': values_label,
                'yaxis_title': 'Strike Price',
                'xaxis': dict(
                    range=[-chart_range, chart_range],
                    zeroline=True,
                    zerolinewidth=2,
                    zerolinecolor='black',
                ),
                'yaxis': dict(
                    autorange='reversed'
                )
            })
            
            # Special handling for bubble charts in horizontal mode
            if graph_type == "Bubble":
                layout_args.update({
                    'hoverlabel': dict(
                        bgcolor="white",
                        font_size=12,
                        font_family="Arial"
                    ),
                    'hovermode': 'closest'
                })

        fig.update_layout(**layout_args)


