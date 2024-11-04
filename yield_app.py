# inference.py
import streamlit as st
import os

from typing import Dict, Tuple, List, Union
from state_manager import StateManager
from yield_prediction import render_yield_advisor_tab
from profit_dashboard import render_profit_dashboard_tab

def main():
    st.set_page_config(
        page_title="Yield Calculator and Profit Dashboard",
        page_icon="🌾",
        layout="wide"
    )

    # Initialize shared state
    StateManager.initialize_state()


    tabs = st.tabs(["Yield Advisor", "Profit Dashboard"])

    with tabs[0]:
        st.title("Yield Advisor")
        st.write("Predict crop yields based on official Indian agricultural data")
        render_yield_advisor_tab()

    with tabs[1]:
        st.title("Profit Dashboard")
        render_profit_dashboard_tab()

# if __name__ == "__main__":
#     # Define your desired port number
#     port = 8510
#     os.system(f"streamlit run yield_app.py --server.port {port}")

main()