import os
import subprocess
import sys

def main():
    # Get the path of the current script
    current_script_path = os.path.abspath(__file__)
    
    # Create a separate streamlit script in the same directory
    streamlit_script_path = os.path.join(os.path.dirname(current_script_path), "snacks_fund_app.py")
    
    # Write the Streamlit app code to the new file
    with open(streamlit_script_path, "w") as f:
        f.write('''
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Snacks Fund Dashboard", layout="wide", page_icon="💰")

# File path hardcoded
file_path = r"C:\\Users\\Navneet Chaudhary\\Desktop\\Fund\\Snacks_Fund.xlsx"

# Check if file exists
if not os.path.exists(file_path):
    st.error(f"Excel file not found at: {file_path}")
    st.info("Please ensure the Excel file exists at the specified location.")
    st.stop()

try:
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    # Ensure required columns exist
    required_columns = ['Date', 'Contributors', 'Spend', 'Contribution', 'Balance']
    for col in required_columns:
        if col not in df.columns:
            st.error(f"Required column '{col}' not found in Excel file")
            st.stop()
    
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # App title and description
    st.title("💰 Snacks Fund Dashboard")
    st.markdown("### Fund Performance and Management Overview")
    
    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_contributions = df['Contribution'].sum()
        st.metric("Total Contributions", f"₹{total_contributions:,.2f}")
    
    with col2:
        total_spending = df['Spend'].sum()
        st.metric("Total Spending", f"₹{total_spending:,.2f}")
    
    with col3:
        current_balance = df['Balance'].iloc[-1] if not df.empty else 0
        st.metric("Current Balance", f"₹{current_balance:,.2f}")
    
    with col4:
        num_contributors = df['Contributors'].nunique()
        st.metric("Number of Contributors", num_contributors)
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Balance over time chart
        st.subheader("Balance Over Time")
        fig_balance = px.line(df, x='Date', y='Balance', markers=True)
        fig_balance.update_layout(xaxis_title="Date", yaxis_title="Balance")
        st.plotly_chart(fig_balance, use_container_width=True)
        
        # Contributions by contributor
        st.subheader("Contributions by Contributor")
        contrib_by_person = df.groupby('Contributors')['Contribution'].sum().reset_index()
        contrib_by_person = contrib_by_person.sort_values('Contribution', ascending=False)
        fig_contrib = px.bar(contrib_by_person, x='Contributors', y='Contribution')
        st.plotly_chart(fig_contrib, use_container_width=True)
    
    with col2:
        # Contributions vs Spending over time
        st.subheader("Contributions vs Spending")
        monthly_data = df.resample('M', on='Date').agg({
            'Contribution': 'sum',
            'Spend': 'sum'
        }).reset_index()
        fig_monthly = go.Figure()
        fig_monthly.add_trace(go.Bar(x=monthly_data['Date'], y=monthly_data['Contribution'], name='Contributions'))
        fig_monthly.add_trace(go.Bar(x=monthly_data['Date'], y=monthly_data['Spend'], name='Spending'))
        st.plotly_chart(fig_monthly, use_container_width=True)
        
        # Pie chart for spending vs contributions
        st.subheader("Total Spending vs Contributions")
        total_contrib = df['Contribution'].sum()
        total_spend = df['Spend'].sum()
        fig_pie = px.pie(values=[total_contrib, total_spend], names=['Contributions', 'Spending'])
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Display detailed transaction data
    st.subheader("Transaction Details")
    
    # Add filters
    col1, col2, col3 = st.columns(3)
    with col1:
        min_date = df['Date'].min().date()
        max_date = df['Date'].max().date()
        start_date = st.date_input("Start Date", min_date)
        end_date = st.date_input("End Date", max_date)
    
    with col2:
        contributors = ['All'] + sorted(df['Contributors'].unique().tolist())
        selected_contributor = st.selectbox("Contributor", contributors)
    
    with col3:
        transaction_type = st.selectbox("Transaction Type", ["All", "Contribution", "Spending"])
    
    # Filter data based on selections
    filtered_df = df.copy()
    filtered_df = filtered_df[(filtered_df['Date'].dt.date >= start_date) & 
                             (filtered_df['Date'].dt.date <= end_date)]
    
    if selected_contributor != 'All':
        filtered_df = filtered_df[filtered_df['Contributors'] == selected_contributor]
    
    if transaction_type == "Contribution":
        filtered_df = filtered_df[filtered_df['Contribution'] > 0]
    elif transaction_type == "Spending":
        filtered_df = filtered_df[filtered_df['Spend'] > 0]
    
    # Display the filtered dataframe
    st.dataframe(filtered_df.style.format({
        'Contribution': '₹{:.2f}',
        'Spend': '₹{:.2f}',
        'Balance': '₹{:.2f}'
    }), use_container_width=True)
    
    # Export functionality
    if st.button("Export Filtered Data"):
        export_path = os.path.join(os.path.dirname(file_path), "exported_fund_data.xlsx")
        filtered_df.to_excel(export_path, index=False)
        st.success(f"Data exported to {export_path}")
    
except Exception as e:
    st.error(f"Error: {str(e)}")
''')

    # Run the streamlit app
    print("Starting Snacks Fund Dashboard...")
    print("This will open in your web browser.")
    print("Press Ctrl+C in this window to exit when done.")
    
    try:
        # Run streamlit as a subprocess
        subprocess.run([sys.executable, "-m", "streamlit", "run", streamlit_script_path], check=True)
    except KeyboardInterrupt:
        print("\nExiting dashboard...")
    except Exception as e:
        print(f"Error running Streamlit: {e}")
        print("\nPlease ensure Streamlit is installed by running:")
        print("pip install streamlit pandas matplotlib plotly openpyxl")
        input("Press Enter to exit...")
    
    print("Dashboard closed.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
