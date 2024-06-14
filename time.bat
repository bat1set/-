@echo off
chcp 65001 >nul
color 0B
set /p time_in=Введите время (в минутах) через которое будет запускаться файл:
set /p repetitions=Введите кол-во повторений:

set /a time_in_seconds=%time_in%*60

call .\.venv\Scripts\activate
for /l %%i in (1, 1, %repetitions%) do (
	color 0B
    timeout /t %time_in_seconds% /nobreak >nul
	echo Время запуска: %time%
    python .\main\main.py
)
pause