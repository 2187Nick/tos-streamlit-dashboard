import plotly.graph_objects as go

class GammaChartBuilder:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def create_empty_chart(self) -> go.Figure:
        """Create initial empty chart"""
        #print("Gamma Chart: create_empty_chart")
        fig = go.Figure()
        self._set_layout(fig, 1, None)  # Use 1 as default range, no price
        return fig

    def create_chart(self, data: dict, strikes: list, option_symbols: list) -> go.Figure:
        """Build and return the gamma exposure chart"""
        fig = go.Figure()
        
        # Get current price first
        current_price = float(data.get(f"{self.symbol}:LAST", 0))
        #print(f"Gamma Chart: create_chart with Current price: {current_price}")
        if current_price == 0:
            return self.create_empty_chart()
        
        pos_gex_values, neg_gex_values = self._calculate_gex_values(data, strikes, option_symbols)

        pos_values = [round(x/1000000, 0) for x in pos_gex_values]
        neg_values = [round(x/1000000, 0) for x in neg_gex_values]

        # Find max values and their strikes
        max_pos_idx = pos_values.index(max(pos_values)) if any(pos_values) else -1
        max_neg_idx = neg_values.index(min(neg_values)) if any(neg_values) else -1
        
        max_pos_strike = strikes[max_pos_idx] if max_pos_idx >= 0 else None
        max_neg_strike = strikes[max_neg_idx] if max_neg_idx >= 0 else None
        
        # Fixed max value calculation with safety checks
        max_pos = max(pos_values) if pos_values else 0
        min_neg = min(neg_values) if neg_values else 0
        max_abs_value = max(abs(min_neg), abs(max_pos))
        
        # Ensure we have a non-zero range
        if max_abs_value == 0:
            max_abs_value = 1
            
        # Add padding to the range (30% on each side)
        padding = max_abs_value * 0.3
        chart_range = max_abs_value + padding

        #print("Gamma Chart: create_chart() done calculating gex values")
        
        self._add_traces(fig, pos_values, neg_values, strikes)
        
        # Add horizontal line for current price
        fig.add_hline(
            y=current_price,
            line_color="blue",
            line_width=2,
            annotation_text=f"${current_price:.2f}",
            annotation_position="top left"
        )

        self._add_annotations(
            fig, max_pos, min_neg, padding,
            max_pos_idx,  max_pos_strike, max_neg_idx, max_neg_strike
        )

        self._set_layout(fig, chart_range, current_price)
        
        return fig

    def _calculate_gex_values(self, data, strikes, option_symbols):
        pos_gex_values = []
        neg_gex_values = []
        
        try:
            underlying_price = float(data.get(f"{self.symbol}:LAST", 0))
        except (ValueError, TypeError):
            underlying_price = 0
            
        if underlying_price == 0:
            return [], []
        
        for strike in strikes:
            try:
                call_symbol = next(sym for sym in option_symbols if f'C{strike}' in sym)
                put_symbol = next(sym for sym in option_symbols if f'P{strike}' in sym)
                #print(f"Call: {call_symbol}")
                
                # Safely get and convert values, defaulting to 0 if any errors
                try:
                    call_gamma = float(data.get(f"{call_symbol}:GAMMA", 0))
                except (ValueError, TypeError):
                    call_gamma = 0
                    
                try:
                    put_gamma = float(data.get(f"{put_symbol}:GAMMA", 0))
                except (ValueError, TypeError):
                    put_gamma = 0
                    
                try:
                    call_oi = float(data.get(f"{call_symbol}:OPEN_INT", 0))
                except (ValueError, TypeError):
                    call_oi = 0
                    
                try:
                    put_oi = float(data.get(f"{put_symbol}:OPEN_INT", 0))
                except (ValueError, TypeError):
                    put_oi = 0
                
                # gamma exposure per $1 change in the underlying price
                # gex = ((call_oi*call_gamma) - (put_oi*put_gamma)) * 100 * underlying_price

                # gamma exposure per 1% change in the underlying price
                gex = ((call_oi*call_gamma) - (put_oi*put_gamma)) * 100 * (underlying_price*underlying_price) * .01

            except Exception:
                # If anything goes wrong with this strike, use 0
                print(f"Error calculating GEX strike: {strike}")
                gex = 0
            
            if gex > 0:
                pos_gex_values.append(gex)
                neg_gex_values.append(0)
            else:
                pos_gex_values.append(0)
                neg_gex_values.append(gex)
        
        #print("pos_gex_values: ", pos_gex_values)
        #print("neg_gex_values: ", neg_gex_values)
        return pos_gex_values, neg_gex_values

    def _add_traces(self, fig, pos_values, neg_values, strikes):
        fig.add_trace(go.Bar(
            x=pos_values,
            y=strikes,
            orientation='h',
            name='Positive GEX',
            marker_color='green'
        ))
        
        fig.add_trace(go.Bar(
            x=neg_values,
            y=strikes,
            orientation='h',
            name='Negative GEX',
            marker_color='red'
        ))

    def _add_annotations(self, fig, max_pos, min_neg, padding, max_pos_idx, max_pos_strike, max_neg_idx, max_neg_strike):
        # Adjust annotation positions based on padding
        annotation_offset = padding * 0.7  # 70% of padding for annotation offset
        
        # Add annotations for max values with adjusted positions
        if max_pos_idx >= 0 and max_pos > 0:
            # Value annotation on the right side of positive bar
            fig.add_annotation(
                x=max_pos,
                y=max_pos_strike,
                text=f"+${round(max_pos)}M",
                showarrow=True,
                arrowhead=2,
                ax=min(40, annotation_offset * 30),
                ay=0,
                align="left"
            )
            # Strike annotation on the left side of positive bar
            fig.add_annotation(
                x=0,  # Position at zero line
                y=max_pos_strike,
                text=f"Strike: {max_pos_strike}",
                showarrow=False,
                xanchor="right",
                xshift=-10  # Shift slightly left of the zero line
            )
        
        if max_neg_idx >= 0 and min_neg < 0:
            # Value annotation on the left side of negative bar
            fig.add_annotation(
                x=min_neg,
                y=max_neg_strike,
                text=f"-${abs(round(min_neg))}M",
                showarrow=True,
                arrowhead=2,
                ax=max(-40, -annotation_offset * 30),
                ay=0,
                align="right"
            )
            # Strike annotation on the right side of negative bar
            fig.add_annotation(
                x=0,  # Position at zero line
                y=max_neg_strike,
                text=f"Strike: {max_neg_strike}",
                showarrow=False,
                xanchor="left",
                xshift=10  # Shift slightly right of the zero line
            )

    def _set_layout(self, fig, chart_range, current_price=None):
        price_str = f" Price: ${current_price:.2f}" if current_price else ""
        fig.update_layout(
            title=f'{self.symbol} Gamma Exposure ($ per 1% move)   {price_str}',
            xaxis_title='Gamma Exposure ($M)',  # Added M to indicate millions
            yaxis_title='Strike Price',
            barmode='overlay',
            showlegend=True,  # Enable legend
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            height=600,
            xaxis=dict(
                range=[-chart_range, chart_range],  # Use padded range
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='black',
            )
        )


