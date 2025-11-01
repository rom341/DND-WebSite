@echo off
echo Activating virtual environment...
call ..\..\..\venv\Scripts\activate.bat

echo Updating Django database...
python ..\manage.py migrate
echo Database updated.

REM call deactivate

pause