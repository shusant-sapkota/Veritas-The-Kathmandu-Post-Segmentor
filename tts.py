from gtts import gTTS
#import pyttsx3
from googletrans import Translator
import os

def tts(text_recieved):
	condition = input("Audio Language? a-English, b= Nepali : ")


	if(condition =='a'):
		speech_generated = gTTS(text=text_recieved,lang='en')
		speech_generated.save("tts.mp3")
		os.startfile('tts.mp3')
		print(text_recieved)

		'''
		engine = pyttsx3.init()
		engine.say(extracted_text)
		engine.setProperty('rate',120)
		engine.setProperty('volume',0.9)
		engine.runAndWait()
		'''

	if(condition =='b'):
		translator = Translator()
		translated = translator.translate(text_recieved, dest='ne')
		print(translated.text)

		speech_generated = gTTS(text=translated.text,lang='ne')
		speech_generated.save("tts.mp3")
		os.startfile('tts.mp3')

	next = input("For next article enter any : ")

	