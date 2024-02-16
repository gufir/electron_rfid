from time import sleep
from os import system
from serial import *
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

relay1 = 17
relay2 = 18

GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)

test_serial = Serial('COM3', 115200, timeout=0.1)
test_serial2 = Serial('COM4', 115200, timeout=0.1)

INVENTORY = 'BB 00 22 00 00 22 7E' #Single Inventory

INVENTORY2 = 'BB 00 27 00 03 22 27 10 83 7E' #MULTIPLE Inventory

STOP = 'BB	00	28	00 00	28	7E' #Stop Multi Inventory

READ = 'BB 00 39 00 09 00 00 00 00 03 00 00 00 02 45 7E' #Read User Memory

VERSION = 'BB 00 03 00 01 00 04 7E'

client = mqtt.Client()

readUserMemory0 = 'BB 00 39 00 09 00 00 00 00 00 00 00 00 07 49 7E'
# 0 Reserved Memory
readUserMemory1 = 'BB 00 39 00 09 00 00 00 00 01 00 00 00 0A 4D 7E'
# 1 EPC 8 - 10 word
readUserMemory2 = 'BB 00 39 00 09 00 00 00 00 02 00 00 00 06 4A 7E'
# 2 TID 6 word
readUserMemory3 = 'BB 00 39 00 09 00 00 00 00 03 00 00 00 02 47 7E'
# 3 user memory 2 word

def send_cmd(cmd):
    data = bytes.fromhex(cmd)
    test_serial.write(data)
    response = test_serial.read(512)
    response_hex = response.hex().upper()
    hex_list = [response_hex[i:i+2] for i in range(0, len(response_hex), 2)]
    hex_space = ' '.join(hex_list)
    
    return hex_space

def send_cmd2(cmd):
    data = bytes.fromhex(cmd)
    test_serial2.write(data)
    response = test_serial2.read(512)
    response_hex = response.hex().upper()
    hex_list = [response_hex[i:i+2] for i in range(0, len(response_hex), 2)]
    hex_space = ' '.join(hex_list)
    
    return hex_space

def connect_to_broker(broker_address, port, username, password):
    broker_address = "127.0.0.1"
    port = 1883
    username = "pi"
    password = "raspberry"

    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.connect(broker_address, port)
    return client

def publish_message(client, topic, message):
    client.publish(topic, message)
    print(f"Published message: {message}")

def turn_on():
    GPIO.output(relay1, GPIO.HIGH)

def turn_on2():
    GPIO.output(relay2, GPIO.HIGH)
    
def turn_off():
    GPIO.output(relay1, GPIO.LOW)

def turn_off2():
    GPIO.output(relay2, GPIO.LOW)

def main():
    terdaftar = 'E8 79 30 00 E2 80 68 94 00 00 40 17 43 54 A1 14 00 00 00 00'
    read1 = send_cmd(readUserMemory1)
    read2 = send_cmd2(readUserMemory1)
    sliced = read1[60:119]
    sliced2 = read2[60:119]
    print(read1)
    if sliced == terdaftar:
        turn_on()
        client.publish("rfid", "FL1")
    else:
        turn_off()
    
    if sliced2 == terdaftar:
        turn_on2()
        client.publish("rfid", "FL1")
    else:
        turn_off2()

if __name__ == '__main__':
    
    while True:
        # read1 = send_cmd(readUserMemory1)
        # print(read1)
        main()
        sleep(0.5)
        system('cls')
