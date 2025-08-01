@echo off
echo Starting eMediCare Server...
echo.
echo Make sure you have Python installed and are in the correct directory.
echo.
cd server\emedicare
echo Current directory: %CD%
echo.
echo Starting Django development server...
echo Server will be available at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver
pause 