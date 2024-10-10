
# SonneControl
A simple discord bot for remote pc control
## Introduction
This python script integrates with discord to manage multiple devices via a discord server and chat is used as if it were a command line
## Features
1) Usable via Discord, so from any device
2) The client is designed to be cross-platform
3) Allows you to access the camera and keyboard to check if someone is using your machine
4) Allows you to execute commands directly in the system terminal, whatever it is
5) Allows you to send and receive files from the client
6) Shows on-screen messages on the client
7) Manages client files (delete, read, encrypt, and decrypt with passwords)


## Installation
Installation is not very complex

1) Create a discord botdi and invite it to a server, if you don't know how to do it follow this guide: https://www.ionos.com/digitalguide/server/know-how/creating-discord-bot/
2) Create a channel named: new-remote. In this channel you will receive the IDs of new devices
3) Back on the discord developer portal in your bot section, go to the bot section and hit “Reset Token,” this will generate a token that you need to enter into the program, so copy it
4) Download the main.py file from this repository

5) Open it and go to the last line of code where it says “YOUR TOKEN” and enter the token you copied in step 3

6) Install all dependencies with this command

#### Windows:
```bash
  pip install tkinter pillow cryptography pyinput pygame pyautogui discord
```
#### GNU/Linux:
```bash
  pip install pillow cryptography pyinput pygame pyautogui discord
```
In linux you must install "Gnome-screenshot" and "tk" whit your package manager

7) Start the script, if all goes well you should see the device ID on the screen and should arrive on the discord channel “new-remote” the code

8) To communicate with that client, you will have to create a channel with the same name as the client ID

9) Try typing into the chat with the “ping” client, if it answers “Pong!” then it works!!!




    
## Commands
