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
from modules.weather import *
from modules.wiki import *
from modules.cinema import *
from data import opts
import webbrowser

# Ассистент говорит

def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()

# Ассистент определяет, ОБРАЩАЕМСЯ ли мы к нему


def callback(voice):
    if voice != None:
        if voice.startswith(opts["alias"]):

            for x in opts['alias']:
                voice = voice.replace(x, '').strip()
            for x in opts['tbr']:
                voice = voice.replace(x, '').strip()

            cmd = recognize_cmd(voice)

            if cmd['cmd'] != '':
                for x in opts['cmds'][cmd['cmd']]:
                    voice = voice.replace(x, '')
                    argument = voice
            else:
                argument = ''
            execute_cmd(cmd['cmd'], argument)







# Распознавание команды

def recognize_cmd(cmd):
    RC = {'cmd' : '', "percent":0}

    for c, v in opts["cmds"].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:

                ###
                RC['cmd'] = c
                RC['percent'] = vrt

    if RC['percent'] < 50:
        RC['cmd'] = ''
    return RC

# Формирование ответа

def execute_cmd(cmd, argument):
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    elif cmd == 'weather':
        speak(weather_main())
    elif cmd == "vk":
        webbrowser.open('https://vk.com/feed', new = 0)
    elif cmd == "cinema":
        speak(get_page_data(get_html()))
    elif cmd == "what is it":
        query = argument
        articles = get_info(get_link(urlgen(query)))
        for title in articles.keys():
            speak(title)
        all_articles = list(articles.keys())
        if not all_articles:
            speak("Информация не найдена")
            return None
        speak("Какой пункт вам нужен?")
        answer = record_voice(None)
        if answer == None:
            answer = 1
        else:
            for x in opts['alias']:
                answer = answer.replace(x, '').strip()
            for x in opts['tbr']:
                answer = answer.replace(x, '').strip()
            if answer.isdigit():
                answer = int(answer)
            elif answer == 'первый':
                answer = 1
            elif answer == 'второй':
                answer = 2
            elif answer == 'третий':
                answer = 3
            else:
                for title in all_articles:
                    if str(answer) in title:
                        print(title)
                        answer = all_articles.index(title) + 1
                        break
                    else:
                        answer = 1
        needed_article = articles[all_articles[answer-1]]
        speak(needed_article[0])
        speak("Перейти по ссылке для подробной информации?")
        if record_voice(None) == 'да':
             webbrowser.open(needed_article[1], new = 0)
        else:
            pass

    else:
        speak("Что вам нужно!")


# Функция для прослушки

def recognition(source, recognizer):
    try:
        audio = recognizer.listen(source)
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Распознано : " + voice)
        return voice
    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
        pass
    except sr.RequestError as e:
        print("[log] Проверьте интернет")
        pass


def record_voice(function):
    with sr.Microphone(device_index = 1) as source:
        r.adjust_for_ambient_noise(source) # recognizer прослушивает 1 секунду и запоминает звук шума, чтобы потом не путать его с твоим голосом
        while True: # Бесконечная прослушка
            time.sleep(0.1)
            if function != None:
                function(recognition(source, r))
            else:
                return recognition(source, r)


#Start

speak_engine = pyttsx3.init()

### Настройка голоса для ассистента (мужской, женский и т.д.)
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[6].id)
###


speak("Добрый день!") # Приветствие

if __name__ == "__main__":
    r = sr.Recognizer()
    record_voice(callback)
