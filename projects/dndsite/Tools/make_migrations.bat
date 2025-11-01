@echo off
REM call venv\Scripts\activate.bat
echo Activating virtual environment...
call ..\..\..\venv\Scripts\activate.bat

echo Making migrations...
python ..\manage.py makemigrations
echo Done.

REM call deactivate

pause