@echo off
cls
echo Do you want the program to run hidden?
set /P pippo="(y/n) "

if "%pippo%"=="y" (
    set comando=pyinstaller --onefile --noconsole
) else if "%pippo%"=="n" (
    set comando=pyinstaller --onefile
) else (
    exit
)

cls
echo Control of dependencies...

pip install tkinter pillow cryptography pyinput pygame pyautogui discord requests

set comando=%comando% --hidden-import pillow --hidden-import requests --hidden-import cryptography main.py

cls
echo Start compilation

%comando%
