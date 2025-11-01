@echo off
echo    Activating virtual environment...
call ..\..\..\venv\Scripts\activate.bat

echo    Creating Django superuser...
python ..\manage.py createsuperuser
echo    Superuser created successfully if no errors occurred.

REM call deactivate

pause