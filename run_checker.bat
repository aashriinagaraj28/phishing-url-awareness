@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if not errorlevel 1 (
    py -3 "%~dp0phishing_checker.py"
) else (
    python "%~dp0phishing_checker.py"
)

echo.
pause
