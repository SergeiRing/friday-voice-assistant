import requests
import time


url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=ed5ab228302bc87016834e2355ae4f2b'

def weather_main():
    town = 'kostomuksha'
    r = requests.get(url.format(town)).json()
    if r['weather'][0]['main'] == 'Clear':
        icon = '☀'
    elif r['weather'][0]['main'] == 'Snow':
        icon = '❄'
    else:
        icon = '💧'
    temp = str(r['main']['temp'])
    description = r['weather'][0]['description']
   # country = r['sys']['country']
   # wind = r['wind']['speed']
   # sunrise = r['sys']['sunrise']
   # sunset = r['sys']['sunset']
   # sunrise = time.strftime('%H : %M', time.localtime(int(sunrise + 60*60*3)))
   # sunset = time.strftime('%H : %M', time.localtime(int(sunset + 60*60*3)))
    if int(temp[-1]) == 1:
        tvar = 'градус'
    elif int(temp[-1]) < 5:
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