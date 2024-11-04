import streamlit as st
class StateManager:
    @staticmethod
    def initialize_state():
        """Initialize shared state variables"""
        if 'total_income_value' not in st.session_state:
            st.session_state.total_income_value = 0.0
        if 'expenses' not in st.session_state:
            st.session_state.expenses = []
        if 'expense_categories' not in st.session_state:
            st.session_state.expense_categories = [
                'Seeds', 'Fertilizers', 'Pesticides', 'Labor', 
                'Equipment', 'Irrigation', 'Transportation', 'Others'
            ]