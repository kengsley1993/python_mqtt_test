import mqtt_pub_sub as mqtt
import speak_test as speaker
import voice_capture as listener
import signal, sys, time

# to stop all the sub-thread and main-thread by ctrl c
def stop_all(*args):
	global speak_loop, voice_looping, main_looping
	speak_loop = False
	voice_looping = False
	main_looping = False
	print("Stop the work")
	sys.exit()

# check the stop case
signal.signal(signal.SIGTERM, stop_all)
signal.signal(signal.SIGINT,  stop_all)

# create mqtt client for connect and sub_pub to EMQ
mqtt.mqtt_client_thread()

# using listener to run audio capture and audio decode
listener.run()

main_looping = True
function_looping = False

# the agant name of the beginning char
name = ['b', 'B', 'P']

while main_looping:
	# if the queue in listener is not empty
	if not listener.que.empty():
		# get the command for queue
		command = listener.que.get()
		print("hear something")
		print(command)
		data = command.split(" ")

		# is it calling the agant name?
		# yes - agant will wait for the control command
		# no - agant will wait for name calling
		if any(elem[0] in name for elem in data) and not function_looping:
			text_to_speech = 'I am listening what your say'
			# text_to_speech = '係'
			speaker.speak(text_to_speech)
			function_looping = True
			data = []
		elif function_looping:
			# if found matched control function
			if "on" in data or "off" in data:
				if "on" in data:
					pin = 1
				elif "off" in data:
					pin = 0
				# send function value to EMQ via mqtt
				mqtt.pub_message(pin)
				function_looping = False
			text_to_speech = 'Get action'
			speaker.speak(text_to_speech)
			data = []
		time.sleep(0.5)