import streamlit as st
from state_manager import StateManager
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime
import pandas as pd
def render_profit_dashboard_tab():
    """Function to render the Profit Dashboard tab content"""
    StateManager.initialize_state()
    
    # Use the shared state value
    total_yield = st.number_input(
        "Total Revenue/Yield (₹)", 
        min_value=0.0, 
        value=st.session_state.total_income_value,
        step=100.0,
        help="This value is automatically populated from your yield predictions. You can adjust it if needed."
    )

    st.header("💰 Profit & Expense Dashboard")
    
    # Initialize session state
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []
    if 'expense_categories' not in st.session_state:
        st.session_state.expense_categories = [
            'Seeds', 'Fertilizers', 'Pesticides', 'Labor', 
            'Equipment', 'Irrigation', 'Transportation', 'Others', 'Cleaning'
        ]
    if 'total_yield_value' not in st.session_state:
        st.session_state.total_yield_value = 0.0
    
    
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []
    if 'expense_categories' not in st.session_state:
        st.session_state.expense_categories = [
            'Seeds', 'Fertilizers', 'Pesticides', 'Labor', 
            'Equipment', 'Irrigation', 'Transportation', 'Others'
        ]
    
    # Get total yield/revenue
    total_yield = st.number_input("Enter Total Revenue/Yield ($)", 
                                 min_value=0.0, 
                                 value=10000.0, 
                                 step=100.0)
    
    # Add expenses section
    st.subheader("Add Expenses")
    
    # New category input
    new_category = st.text_input("Add New Category (Optional)")
    if new_category and new_category not in st.session_state.expense_categories:
        st.session_state.expense_categories.append(new_category)
        st.success(f"Added new category: {new_category}")
    
    # Expense form
    # Expense form
    with st.form("expense_form"):
        st.write("Enter Your Expenses:")
        temp_expenses = []
        
        # Create 5 rows of expense inputs
        for i in range(5):
            col1, col2, col3 = st.columns([2, 2, 2])
            
            with col1:
                name = st.selectbox(
                    f"Category {i+1}",
                    options=[''] + st.session_state.expense_categories,
                    key=f"cat_{i}"
                )
            
            with col2:
                description = st.text_input(
                    f"Description {i+1}",
                    key=f"desc_{i}"
                )
            
            with col3:
                amount = st.number_input(
                    f"Amount {i+1} ($)",
                    min_value=0.0,
                    step=10.0,
                    key=f"amount_{i}"
                )
            
            if name and amount > 0:
                temp_expenses.append({
                    'category': name,
                    'description': description,
                    'amount': amount,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        
        submitted = st.form_submit_button("Add Expenses")
        if submitted and temp_expenses:
            st.session_state.expenses.extend(temp_expenses)
            st.success(f"Successfully added {len(temp_expenses)} expenses!")
    
    # Display analytics if there are expenses
    if st.session_state.expenses:
        df_expenses = pd.DataFrame(st.session_state.expenses)
        
        # Calculate metrics
        total_expenses = df_expenses['amount'].sum()
        profit = total_yield - total_expenses
        profit_margin = (profit / total_yield * 100) if total_yield > 0 else 0
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Revenue", f"${total_yield:,.2f}")
        with col2:
            st.metric("Total Expenses", f"${total_expenses:,.2f}", 
                     delta=-total_expenses, 
                     delta_color="inverse")
        with col3:
            st.metric("Net Profit", f"${profit:,.2f}", 
                     delta=f"{profit_margin:.1f}% margin")
        
        # Visualizations
        st.subheader("Financial Analysis")
        
        # Revenue breakdown pie chart
        fig_pie = px.pie(
            values=[profit, total_expenses],
            names=['Profit', 'Expenses'],
            title='Revenue Breakdown',
            color_discrete_sequence=['green', 'red']
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Expenses by category bar chart
        fig_bar = px.bar(
            df_expenses.groupby('category')['amount'].sum().reset_index(),
            x='category',
            y='amount',
            title='Expenses by Category'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Expense table
        st.subheader("Expense History")
        
        # Category filter
        selected_category = st.selectbox(
            "Filter by Category",
            options=['All'] + list(df_expenses['category'].unique())
        )
        
        # Filter data
        filtered_df = df_expenses if selected_category == 'All' else \
                     df_expenses[df_expenses['category'] == selected_category]
        
        # Display table
        st.dataframe(
            filtered_df.style.format({'amount': '${:,.2f}'}),
            column_config={
                "category": "Category",
                "description": "Description",
                "amount": "Amount",
                "date": "Date Added"
            },
            hide_index=True
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download Expense Data",
            data=csv,
            file_name="expenses.csv",
            mime="text/csv"
        )
        
        # Clear button
        if st.button("Clear All Expenses"):
            st.session_state.expenses = []
            st.experimental_rerun()
    
    else:
        st.info("No expenses added yet. Start by adding your expenses using the form above!")





    
        