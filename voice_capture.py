import speech_recognition as sr
import signal
import threading
import sys
from queue import Queue

r = sr.Recognizer()
r.dynamic_energy_threshold = False
r.energy_threshold = 200
# print(r.dynamic_energy_threshold)
# print(r.energy_threshold)
mic = sr.Microphone()
voice_looping = False
audio = None
timeout = 2
que = Queue()

# Sub-thread: use to capture the audio from microphone
class voice_listen(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global voice_looping, audio, timeout, mic, r
		# c.acquire()
		voice_looping = True
		while voice_looping:
			try:
				if (not audio):
					print("Starting")
					print("Current ", timeout)
					with mic as source:
						# r.adjust_for_ambient_noise(source, duration=0.5)
						audio = r.listen(source, timeout=timeout)
						# print(audio)
				time.sleep(0.1)
			except:
				pass

# Sub-thread: speech to text by using google
class voice_decode(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global voice_looping, audio, r, que
		voice_looping = True
		while voice_looping:
			try:
				if (audio):
					command = r.recognize_google(audio)
					audio = None
					que.put(command)
					time.sleep(0.5)
			except:
				# print("error in decode")
				audio = None
				pass

# Group and run voice listener
def run():
	listen = voice_listen()
	decode = voice_decode()

	listen.setDaemon(True)
	decode.setDaemon(True)

	listen.start()
	decode.start()


if __name__ == '__main__':
	def stop_all(*args):
		global voice_looping
		voice_looping = False
		print("Stop the work")
		sys.exit()

	voice_looping = True

	# print(sr.Microphone.list_microphone_names())
	signal.signal(signal.SIGTERM, stop_all)
	# signal.signal(signal.SIGQUIT, stop_all)
	signal.signal(signal.SIGINT,  stop_all)  # Ctrl-C

	run()

	# print(listen.isAlive())
	# print(decode.isAlive())

	while True:
		if not que.empty():
			result = que.get()
			print("HIIIIII")
			print(result)