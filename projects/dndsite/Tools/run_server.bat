@echo off
echo Activating virtual environment...
call ..\..\..\venv\Scripts\activate.bat

echo Starting Django development server (http://127.0.0.1:8000/)...
python ..\manage.py runserver

REM call deactivate