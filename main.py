import os
import eel

from engine.features import *
from engine.command import *
from engine.auth import recoganize
def start():
    
    eel.init("www")

    playAssistantsound()
    @eel.expose
    def init():
        subprocess.call([r'device.bat'])
        eel.hideLoader() # type: ignore
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth() # type: ignore
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess() # type: ignore
            speak("Hello, Welcome Sir, How can i Help You")
            eel.hideStart() # type: ignore
            playAssistantsound()
        else:
            speak("Face Authentication Fail")
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True)