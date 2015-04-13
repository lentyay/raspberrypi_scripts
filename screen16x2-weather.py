#!/usr/bin/python

# Example script for article http://newkamikaze.com/articles/76
#
# Uses 16 x 2 LCD + Keypad
# Requires RPi.GPIO & Adafruit charLCD classes
# https://pypi.python.org/pypi/RPi.GPIO
# https://github.com/adafruit/Adafruit_Python_CharLCD

import json
import urllib2
from time import sleep
import Adafruit_CharLCD as LCD


lcd = LCD.Adafruit_CharLCDPlate()
lcd.set_color(0, 0, 0)

# Create some custom degree characters
lcd.create_char(1, [24,24,3,4,4,4,3,0])

# Cyrillic transliteration
cyrillic_translit = {
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

def transliterate(word, translit_table):
    converted_word = ''
    for char in word:
        transchar = ''
        if char in translit_table:
            transchar = translit_table[char]
        else:
            transchar = char
        converted_word += transchar
    return converted_word


while True:
	# Get weather data
	data = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/find?q=Tallinn&units=metric&lang=ru'))

	# LED blinking after update
	while True:
		lcd.set_color(0, 1, 0)
		sleep(0.1)
		lcd.set_color(0, 0, 0)
		break

	# Clear screen and output data
	lcd.clear()
	lcd.message(data['list'][0]['name'] + " " + str(data['list'][0]['main']['temp']) + "\x01 \n" + transliterate(unicode(data['list'][0]['weather'][0]['description']), cyrillic_translit))

	sleep(600)