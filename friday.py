# Voice Assistant `Friday` version Alpha 1.0 by Spider-man
# Based on the Priler assistant

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
from modules.weather import weather_main
import webbrowser


opts = {
    "alias":("пятница", "пятый", "пятниц"), # Обращения к ассистенту
    "tbr" : ("скажи", "расскажи", "покажи", "сколько", "какая"), # Слова, которые нужно убирать из команды
    "cmds": {
        "ctime" : ("текущее время", "сейчас времени", "который час"), # Команда и слова, по которым она определяется
        "weather" : ("погода", "погодка", "что на улице"),
        "vk" : ("открой вк", "вк", "вконтакте", "в контакте")
    }
}


# Ассистент говорит

def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()

# Ассистент определяет, ОБРАЩАЕМСЯ ли мы к нему

def callback(voice):
    if voice.startswith(opts["alias"]):
        cmd = voice

        for x in opts["alias"]:
            cmd = cmd.replace(x, "").strip()
        for x in opts['tbr']:
            cmd = cmd.replace(x, "").strip()

        cmd = recognize_cmd(cmd)
        execute_cmd(cmd['cmd'])

# Распознавание команды

def recognize_cmd(cmd):
    RC = {'cmd' : '', "percent":0}

    for c, v in opts["cmds"].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC

# Формирование ответа

def execute_cmd(cmd):
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    elif cmd == 'weather':
        speak(weather_main())
    elif cmd == "vk":
        webbrowser.open('https://vk.com/feed', new = 0)
    else:
        speak("Что вам нужно!")


# Функция для прослушки

def audition(source, recognizer):
    try:
        audio = r.listen(source)
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Распознано : " + voice) 
        callback(voice)   
    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Проверьте интернет") 

#Start

speak_engine = pyttsx3.init()

### Настройка голоса для ассистента (мужской, женский и т.д.)
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[6].id)
###


speak("Добрый день!") # Приветствие

if __name__ == "__main__":
    r = sr.Recognizer()
    with sr.Microphone(device_index = 1) as source:
        r.adjust_for_ambient_noise(source) # recognizer прослушивает 1 секунду и запоминает звук шума, чтобы потом не путать его с твоим голосом
        while True: # Бесконечная прослушка
            time.sleep(0.1)
            audition(source, r)
