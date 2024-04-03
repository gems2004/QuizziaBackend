@echo off

:start
cls
set mypath=%cd%
@echo %mypath%

python -m venv venv

call .\venv\Scripts\activate
pip install -r .\Quiz\requirements.txt


@echo Starting server and Opening browser...
timeout /t 5 /nobreak

start "" http://127.0.0.1:8000
python .\Quiz\manage.py runserver 8000
pause
exit