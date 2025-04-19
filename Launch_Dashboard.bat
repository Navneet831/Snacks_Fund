@echo off
echo Starting Snacks Fund Dashboard...
echo This will open in your web browser.
echo Press Ctrl+C in this window to exit when done.

cd %~dp0
streamlit run snacks_fund_app.py

pause
