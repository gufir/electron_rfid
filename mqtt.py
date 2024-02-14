import paho.mqtt.client as mqtt

# Define callback functions for connection and message events
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Failed to connect, return code: ", rc)

def on_publish(client, userdata, mid):
    print("Message published")

# Create an MQTT client instance
client = mqtt.Client()

# Set username and password for authentication
username = "pi"
password = "raspberry"
client.username_pw_set(username, password)

# Set callback functions
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the MQTT broker
broker_address = "192.168.161.64"
port = 1883
client.connect(broker_address, port)

# Publish a message
topic = "rfid"
message = "Hello, MQTT!"
client.publish(topic, message)

# Loop to maintain network traffic
client.loop_forever()
