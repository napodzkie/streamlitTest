@echo off
echo Starting CivicGuardian App...
echo.
echo Opening app in your default browser...
start "" "index.html"
echo.
echo If the app doesn't load properly, try one of these solutions:
echo.
echo 1. Install Python and run: python -m http.server 8000
echo 2. Install Node.js and run: npx http-server -p 8000
echo 3. Use VS Code Live Server extension
echo 4. Use any other local web server
echo.
echo Press any key to exit...
pause > nul
