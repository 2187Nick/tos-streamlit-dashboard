import streamlit as st
from datetime import date, timedelta

class DashboardLayout:
    @staticmethod
    def _get_nearest_friday(from_date=None):
        """Get the nearest Friday from a given date"""
        if from_date is None:
            from_date = date.today()
        
        # If today is Friday (weekday 4), return today's date
        if from_date.weekday() == 4:
            return from_date
        
        # Get days until next Friday
        days_ahead = 4 - from_date.weekday()
        if days_ahead <= 0:  # If weekend
            days_ahead += 7
        return from_date + timedelta(days_ahead)

    @staticmethod
    def setup_page():
        """Setup basic page layout"""
        st.title("Live Options Dashboard")
        # Add any other layout setup that isn't page config
        
        st.markdown(DashboardLayout._get_custom_css(), unsafe_allow_html=True)

    @staticmethod
    def create_input_section():
        col1, col2, col3, col4, col5, button_col = st.columns([2, 2, 2, 2, 2, 1])

        with col1:
            symbol = st.text_input("Symbol:", value="SPY").upper()
        with col2:
            expiry_date = st.date_input(
                "Expiry Date:",
                # Default to the nearest Friday
                value=DashboardLayout._get_nearest_friday(),
                format="MM/DD/YYYY"
            )
        with col3:
            strike_range = st.number_input("Strike Range $(±)", value=10, min_value=1, max_value=500)
        with col4:
            strike_spacing = st.selectbox(
                "Strike Spacing",
                options=[0.5, 1.0, 2.5, 5.0, 10.0, 25.0],
                index=1  # Default to 1.0
            )
        with col5:
            refresh_rate = st.number_input(
                "Refresh Rate (s)",
                value=15,
                min_value=1,
                max_value=300,
                help="Chart refresh interval in seconds"
            )
        with button_col:
            # Add vertical padding and width control in the same div
            st.markdown('<div style="padding-top: 28px; width: 125px;">', unsafe_allow_html=True)
            toggle_button = st.button(
                "Pause" if st.session_state.get('initialized', False) else "Start",
                icon="⏸️" if st.session_state.get('initialized', False) else "🔥",
            )
            st.markdown('</div>', unsafe_allow_html=True)

        return symbol, expiry_date, strike_range, strike_spacing, round(refresh_rate/2), toggle_button

    @staticmethod
    def _get_custom_css():
        return """
        <style>
            [data-testid="stStatusWidget"] {visibility: hidden;}
            .stDeployButton {
                visibility: hidden;
            }
            div.stButton > button {
                width: 125px;  /* or use 100% for full width */
            }
        </style>
        """
