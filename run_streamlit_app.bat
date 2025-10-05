@echo off
echo Installing required packages...
pip install -r requirements.txt

echo.
echo Starting CivicGuardian Streamlit App...
echo.
echo The app will open in your browser automatically.
echo If it doesn't open, go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server when you're done.
echo.

streamlit run civicguardian_app.py
