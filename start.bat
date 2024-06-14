@echo off
color 0B
chcp 65001 >nul
call .\.venv\Scripts\activate
python .\main\main.py
pause