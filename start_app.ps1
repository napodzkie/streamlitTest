Write-Host "Starting CivicGuardian App..." -ForegroundColor Green
Write-Host ""
Write-Host "Opening app in your default browser..." -ForegroundColor Yellow

# Open the HTML file in the default browser
Start-Process "index.html"

Write-Host ""
Write-Host "If the app doesn't work properly, you need a local web server." -ForegroundColor Red
Write-Host ""
Write-Host "Quick Solutions:" -ForegroundColor Cyan
Write-Host "1. Install Python from Microsoft Store, then run: python -m http.server 8000" -ForegroundColor White
Write-Host "2. Install Node.js from nodejs.org, then run: npx http-server -p 8000" -ForegroundColor White
Write-Host "3. Use VS Code with Live Server extension" -ForegroundColor White
Write-Host "4. Use any web server software" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
