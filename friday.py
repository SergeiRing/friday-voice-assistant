# Voice Assistant `Friday` version Alpha 1.0 by Spider-man
# Is developing as extend of Priler Assistant 

# Uses :
# speech_recognition
# PyAudio
# pyttsx3
# fuzzywuzzy


import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

opts = {
    "alias":("пятница", "пятый", "пятниц"),
    "tbr" : ("скажи", "расскажи", "покажи"),
    "cmds": {
        "ctime" : ("текущее время", "сейчас времени", "который час")
    }
}


def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Распознано " + voice)

        if voice.startswith(opts["alias"]):
            cmd = voice

            for x in opts["alias"]:
                cmd = cmd.replace(x, "").strip()
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            cmd = recognize_cmd(cmd)
            execute_cmd(cmd)

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] проверьте интернет") 

def recognize_cmd(cmd):
    RC = {'cmd' : '', "percent":0}

    for c, v in opts["cmds"].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC


def execute_cmd(RC):
    if RC["cmd"] == 'ctime':
        now = datetime.datetime.now()
        speak("Now is " + str(now.hour) + ":" + str(now.minute))


#Start
r = sr.Recognizer()
m = sr.Microphone(device_index = 1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()


speak("Hello")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1)
