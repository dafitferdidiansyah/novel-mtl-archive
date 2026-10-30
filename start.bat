@echo off
echo ========================================================
echo   Starting EPUB Downloader (Backend + Frontend)
echo ========================================================

start "EPUB Backend (Django)" cmd /k "cd /d "%~dp0backend" && .venv\Scripts\activate && python manage.py runserver 0.0.0.0:8000"

timeout /t 2 >nul

start "EPUB Frontend (Vite)" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo Backend running on  : http://localhost:8000
echo Frontend running on : http://localhost:5174
echo ========================================================
