Write-Host "Installing required packages..." -ForegroundColor Green
pip install -r requirements.txt

Write-Host ""
Write-Host "Starting CivicGuardian Streamlit App..." -ForegroundColor Yellow
Write-Host ""
Write-Host "The app will open in your browser automatically." -ForegroundColor Cyan
Write-Host "If it doesn't open, go to: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server when you're done." -ForegroundColor Red
Write-Host ""

streamlit run civicguardian_app.py
