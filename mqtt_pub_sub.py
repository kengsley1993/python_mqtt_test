import paho.mqtt.client as mqtt

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
	print("Connect with result code " + str(rc))

	# subscrible the topic to listen
	client.subscribe("esp8266/test")

# receive the message from EMQ serivce
def on_message(client, userdata, msg):
	print("Receive message: ")
	print(msg.topic + " " + msg.payload.decode('utf-8'))

# pub the message to EMQ serivce
def pub_message(data, topic="esp8266/test"):
	client.publish(topic, payload=data, qos=0)

def mqtt_client_thread():
	# init client
	client_id = "esp8266_test"

	# setting the connection of client
	client.on_connect = on_connect

	# setting the receive message of client
	client.on_message = on_message

	# setting the username and password of client
	mqtt_username = "steven"
	mqtt_password = "On99a55s66"
	client.username_pw_set(mqtt_username, mqtt_password)

	# setting the connection IP and port
	print("Start to connect ...")
	mqtt_ip = "47.107.79.52"
	mqtt_port = 1883
	client.connect(mqtt_ip, mqtt_port, 60)

	# client.loop_forever()
	client.loop_start()

if __name__ == '__main__':
	mqtt_client_thread()

	import random
	import time

	while True:
		temp = random.randint(0, 40)
		pub_message(temp)
		time.sleep(5)