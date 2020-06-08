import pyttsx3
import time
import signal
import sys

# voice database
voice_hk = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_zh-HK_HunYee_11.0'
voice_cn = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_zh-CN_HuiHui_11.0'
voice_en = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

# start up the TTS engine
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('voice', voice_en)
engine.setProperty('rate', rate-30)

def speak(text_to_speech):
	try:
		if (text_to_speech != ''):
			engine.say(text_to_speech)
			text_to_speech = ''
			engine.runAndWait()
			print("end of talking")
			time.sleep(0.5)
	except:
		print("error in speak")
		pass

if __name__ == '__main__':
	def stop_all(*args):
		global speak_loop
		speak_loop = False
		print("Stop the work")
		sys.exit()

	signal.signal(signal.SIGTERM, stop_all)
	signal.signal(signal.SIGINT,  stop_all)

	speak_loop = True

	while speak_loop:
		speak('hello')