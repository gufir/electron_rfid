from time import sleep
from os import system
from serial import *
import paho.mqtt.client as mqtt

test_serial = Serial('COM4', 115200, timeout=0.1)

INVENTORY = 'BB 00 22 00 00 22 7E' #Single Inventory

INVENTORY2 = 'BB 00 27 00 03 22 27 10 83 7E' #MULTIPLE Inventory

STOP = 'BB 00 28 00 00 28 7E' #Stop Inventory

READ = 'BB 00 39 00 09 00 00 FF FF 03 00 00 00 02 45 7E' #Read User Memory

readUserMemory0 = 'BB 00 39 00 09 00 00 00 00 00 00 00 00 07 49 7E'
# 0 Reserved Memory
readUserMemory1 = 'BB 00 39 00 09 00 00 00 00 01 00 00 00 0A 4D 7E'
# 1 EPC 8 - 10 word
readUserMemory2 = 'BB 00 39 00 09 00 00 00 00 02 00 00 00 06 4A 7E'
# 2 TID 6 word
readUserMemory3 = 'BB 00 39 00 09 00 00 00 00 03 00 00 00 02 47 7E'
# 3 user memory 2 word

# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("Connected to broker")
#     else:
#         print("Connection failed")

# def connect_to_broker(broker_address, port, username, password):
#     client = mqtt.Client()
#     client.username_pw_set(username, password)
#     client.on_connect = on_connect
#     client.connect(broker_address, port)
#     return client

# def publish_message(client, topic, message):
#     client.publish(topic, message)
#     print(f"Published message: {message}")

def send_cmd(cmd):
    data = bytes.fromhex(cmd)
    test_serial.write(data)
    response = test_serial.read(512)
    response_hex = response.hex().upper()
    hex_list = [response_hex[i:i+2] for i in range(0, len(response_hex), 2)]
    hex_space = ' '.join(hex_list)
    print(hex_space)

# def main():
#     broker_address = "192.168.161.64"
#     port = 1883
#     username = "pi"
#     password = "raspberry"

#     client = connect_to_broker(broker_address, port, username, password)
#     topic = "rfid"
#     client.subscribe(topic)
    
#     send_cmd(INVENTORY)
#     read = send_cmd(READ)

#     MSG = read

#     publish_message(client, topic, MSG)
#     client.loop_forever()


# if __name__ == '__main__':
#     while True:
#         sleep(0.5)
#         system('cls')

if __name__ == '__main__':
    while True:
        send_cmd(INVENTORY)
        sleep(0.5)
        system('cls')



