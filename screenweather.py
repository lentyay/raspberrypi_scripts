#!/usr/bin/python

# Improved version of screen16x2-weather.py
# Features:
#   Current weather condition
#   Weather forecast for 1 week (days switches by left/right buttons)
#   Auto-return to main screen after 5 seconds (adjustable)
#   Logging
#
# Uses 16 x 2 LCD + Keypad
# Requires RPi.GPIO & Adafruit charLCD classes
# https://pypi.python.org/pypi/RPi.GPIO
# https://github.com/adafruit/Adafruit_Python_CharLCD

import json
import urllib2
import time
import Adafruit_CharLCD as LCD
import datetime
import logging

logging.basicConfig(filename='screenweather.log',level=logging.INFO)

city_name = 'Tallinn'
interval_screen = 5
interval_data = 10 * 60
timer_screen = time.time()
timer_data = time.time()

data = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/find?q=' + city_name + '&units=metric&lang=ru'))
forecast = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/forecast/daily?q=' + city_name + '&units=metric&lang=ru'))

lcd = LCD.Adafruit_CharLCDPlate()
lcd.set_color(0, 0, 0)

# create some custom characters
# Degree
lcd.create_char(1, [24,24,3,4,4,4,3,0])

# Make list of button value, text, and backlight color.
buttons = ( (LCD.SELECT, 'Select', (1,1,1)),
            (LCD.LEFT,   'Left'  , (1,0,0)),
            (LCD.UP,     'Up'    , (0,0,1)),
            (LCD.DOWN,   'Down'  , (0,1,0)),
            (LCD.RIGHT,  'Right' , (1,0,1)) )
    
forecast_days = [u'Сегодня', u'Завтра', u'Послезавтра', u'Через 2 дня', u'Через 3 дня', u'Через 4 дня', u'Через 5 дней']
forecast_day = 1

translit_table = {
    u'\u0410': 'A', u'\u0430': 'a',
    u'\u0411': 'B', u'\u0431': 'b',
    u'\u0412': 'V', u'\u0432': 'v',
    u'\u0413': 'G', u'\u0433': 'g',
    u'\u0414': 'D', u'\u0434': 'd',
    u'\u0415': 'E', u'\u0435': 'e',
    u'\u0416': 'Zh', u'\u0436': 'zh',
    u'\u0417': 'Z', u'\u0437': 'z',
    u'\u0418': 'I', u'\u0438': 'i',
    u'\u0419': 'J', u'\u0439': 'j',
    u'\u041a': 'K', u'\u043a': 'k',
    u'\u041b': 'L', u'\u043b': 'l',
    u'\u041c': 'M', u'\u043c': 'm',
    u'\u041d': 'N', u'\u043d': 'n',
    u'\u041e': 'O', u'\u043e': 'o',
    u'\u041f': 'P', u'\u043f': 'p',
    u'\u0420': 'R', u'\u0440': 'r',
    u'\u0421': 'S', u'\u0441': 's',
    u'\u0422': 'T', u'\u0442': 't',
    u'\u0423': 'U', u'\u0443': 'u',
    u'\u0424': 'F', u'\u0444': 'f',
    u'\u0425': 'Kh', u'\u0445': 'kh',
    u'\u0426': 'Ts', u'\u0446': 'ts',
    u'\u0427': 'Ch', u'\u0447': 'ch',
    u'\u0428': 'Sh', u'\u0448': 'sh',
    u'\u0429': 'Shch', u'\u0449': 'shch',
    u'\u042a': '"', u'\u044a': '"',
    u'\u042b': 'Y', u'\u044b': 'y',
    u'\u042c': "'", u'\u044c': "'",
    u'\u042d': 'E', u'\u044d': 'e',
    u'\u042e': 'Ju', u'\u044e': 'ju',
    u'\u042f': 'Ja', u'\u044f': 'ja'
}

def transliterate(word):
    converted_word = ''
    for char in word:
        transchar = ''
        if char in translit_table:
            transchar = translit_table[char]
        else:
            transchar = char
        converted_word += transchar
    return converted_word    


def weather_current():
    message = data['list'][0]['name'] + " " + str(data['list'][0]['main']['temp']) + "\x01 \n" + transliterate(unicode(data['list'][0]['weather'][0]['description'])).capitalize()
    return message

def weather_forecast(day):
    message = transliterate(forecast_days[day]) + "\n" + str(int(forecast['list'][day]['temp']['day'])) + "\x01 " + transliterate(unicode(forecast['list'][day]['weather'][0]['description'])).capitalize()
    return message

def forecast_day_set(button):
    global forecast_day
    if button == 1:
        forecast_day = forecast_day + 1

    if button == 4:
        forecast_day = forecast_day - 1

    if forecast_day < 1:
        forecast_day = 1

    if forecast_day > 6:
        forecast_day = 6
        
def update_screen(content, led, log_message):
    lcd.set_color(led[0], led[1], led[2])
    time.sleep(0.1)
    lcd.set_color(0, 0, 0)
    lcd.clear()
    lcd.message(content)
    logging.info(str(datetime.datetime.now()) + ' ' + log_message)
    
def update_data():
    logging.info(str(datetime.datetime.now()) + ' data updated')
    lcd.set_color(1, 0, 0)
    time.sleep(0.1)
    lcd.set_color(0, 0, 0)
    data = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/find?q=' + city_name + '&units=metric&lang=ru'))
    forecast = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/forecast/daily?q=' + city_name + '&units=metric&lang=ru'))
    update_screen(weather_current(), (0,1,0), 'updated current weather after data update')

    
update_screen(weather_current(), (0,1,0), 'initial update')

displayed_current = True

while True:
    for button in buttons:
        delta_screen = time.time() - timer_screen
        delta_data = time.time() - timer_data
            
        if delta_screen >= interval_screen and displayed_current == False:
            displayed_current = True
            forecast_day = 1
            timer_screen = time.time()
            update_screen(weather_current(), (0,1,0), 'displayed current weather')

        if delta_data >= interval_data:
            timer_data = time.time()
            update_data()

        if lcd.is_pressed(button[0]):
            displayed_current = False
            timer_screen = time.time()
            update_screen(weather_forecast(forecast_day), button[2], 'displayed forecast for day ' + str(forecast_day))
            forecast_day_set(button[0]);
            
        #print delta
        time.sleep(0.05)
        