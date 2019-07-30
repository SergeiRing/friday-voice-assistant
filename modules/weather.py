import requests
import time
from data import urls


url = urls['openweathermap']

def weather_main():
    town = 'kostomuksha'
    r = requests.get(url.format(town)).json()
    temp = str(r['main']['temp'])
    description = r['weather'][0]['description']
   # country = r['sys']['country']
   # wind = r['wind']['speed']
   # sunrise = r['sys']['sunrise']
   # sunset = r['sys']['sunset']
   # sunrise = time.strftime('%H : %M', time.localtime(int(sunrise + 60*60*3)))
   # sunset = time.strftime('%H : %M', time.localtime(int(sunset + 60*60*3)))
    if int(str(int(float(temp)))[-1]) == 1:
        tvar = 'градус'
    elif int(str(int(float(temp)))[-1]) < 5 and int(str(int(float(temp)))[-1]) != 0:
        tvar = 'градуса'
    else:
        tvar = 'градусов'

    if 'cloud' in description:
        dvar = 'облачно'
    elif 'sun' in description:
        dvar = 'солнечно'
    elif 'rain' in description:
        dvar = "дождь"
    elif 'snow' in description:
        dvar = "снег"
    elif 'clear' in description:
        dvar = 'чистое небо'


    return 'На улице : {}\n{} {}'.format(dvar, int(float(temp)), tvar)