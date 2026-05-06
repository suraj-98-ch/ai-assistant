import os
import re
from shlex import quote
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pvporcupine
import pyaudio 
from engine.command import speak
from engine.config import ASSISTANT_NAME
# playsound
import pywhatkit as kit
import pyautogui as autogui
from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat
#sql here
con = sqlite3.connect("jarvis.db")
cursor = con.cursor()


@eel.expose
def playAssistantsound():
    music_dir ="C:\\Users\\Chetan\\OneDrive\\Desktop\\rrr\\www\\assets\\audio\\start sound.mp3"
    playsound(music_dir)


def openCommand(query):
    query =query.replace(ASSISTANT_NAME,"")
    query =query.replace("open","")
    query =query.lower()
    
    app_name = query.strip()

    if app_name !="":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name=?' ,(app_name,))
            results = cursor.fetchall()

            if len (results) !=0:
                speak("opening"+query)
                os.startfile(results[0][0])

            elif len (results)==0:
                cursor.execute(
                'SELECT url FROM web_command WHERE name=?',(app_name,))
                results = cursor.fetchall()

                if len (results) !=0:
                    speak("Opening"+query)
                    webbrowser.open(results[0][0])
                else:
                    speak("Opening"+query)
                    try:
                        os.system('start'+query)
                    except:
                        speak("application not found")
        except:
            speak("some thing went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing " +search_term+"on YouTube") # type: ignore
    kit.playonyt(search_term) # type: ignore

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
        # pre trained keywords
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"])
        paud = pyaudio.PyAudio() # type: ignore
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        print("Listening for wake words...")
        #loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length,exception_on_overflow=False)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            #processing keyword come from mic 
            keyword_index=porcupine.process(keyword)
            #checking first keyword detetcted for not 
            if keyword_index>=0:
                print("Hotword detected")

                #pressing shorcut key win+j
                
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
    except :
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# find contacts
def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
# whatsapp meswded
def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    autogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        autogui.hotkey('tab')

    autogui.press('enter')
    speak(jarvis_message)
 #chat bot
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine/cookies.json") # type: ignore
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response = chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

# android automation 
def makeCall(name,mobileNo):
    mobileNo = mobileNo.replace(" ","")
    speak("calling"+name)
    command = 'adb shell  am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)

# to send message 
def sendMessage(message,mobileNo,name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app 
    tapEvents(164, 2227) 
    #start chat 
    tapEvents(964,2217)
    #search mobile no
    adbInput(mobileNo)
    #tap on name 
    tapEvents(229,772)
    # tap on input box
    tapEvents(278,1386)
    #message
    adbInput(message)
    #send 
    tapEvents(990,1430)
    speak("message send sucessfully to "+name )

