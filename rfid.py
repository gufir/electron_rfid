from time import sleep
from os import system
from serial import *
import mysql.connector
from datetime import datetime
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt_client


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
relay1 = 14
relay2 = 15

GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)

def on_relay(relay):
    GPIO.output(relay, GPIO.HIGH)

def off_relay(relay):
    GPIO.output(relay, GPIO.LOW)

def insert_db(status):

    mydb = mysql.connector.connect(
    host="raspberrypi.local",
    user="pi",
    password="raspberry",
    database="Dojo"
)
    now = datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    mycursor = mydb.cursor()
    query = "INSERT INTO Conveyor (DATE_TIME,STATUS) VALUES (%s,%s)"
    mycursor.execute(query,(now,status))
    mydb.commit()

    return print("Insert Success")

test_serial = Serial('/dev/ttyUSB0', 115200, timeout=0.1)
test_serial2 = Serial('/dev/ttyUSB1', 115200, timeout=0.1)

INVENTORY = 'BB 00 22 00 00 22 7E' #Single Inventory

INVENTORY2 = 'BB 00 27 00 03 22 27 10 83 7E' #MULTIPLE Inventory

STOP = 'BB	00	28	00 00	28	7E' #Stop Multi Inventory

READ = 'BB 00 39 00 09 00 00 00 00 03 00 00 00 02 45 7E' #Read User Memory

VERSION = 'BB 00 03 00 01 00 04 7E'

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

def main():
    terdaftar = 'E8 79 30 00 E2 80 68 94 00 00 40 17 43 54 A1 14 00 00 00 00'
    terdaftar1 = '19 63 30 00 E2 80 68 94 00 00 50 17 43 54 A1 4F 00 00 00 00'
    terdaftar2 = '19 63 30 00 E2 80 68 94 00 00 50 17 43 54 A1 4F 00 00 00 00'
    read1 = send_cmd(readUserMemory1)
    sliced = read1[60:119]
    print(read1)
    if sliced == terdaftar1:
        status = "1"
        insert_db(status)
        on_relay(relay1)

    read2 = send_cmd2(readUserMemory1)
    sliced2 = read2[60:119]
    print(read2)

    if sliced2 == terdaftar1:
        status = "0"
        insert_db(status)
        off_relay(relay1)


if __name__ == '__main__':
    while True:
        # read1 = send_cmd(readUserMemory1)
        # print(read1)
        main()
        sleep(0.5)
        system('clear')

# main()
# off_relay(relay1)
        
# var = send_cmd(readUserMemory1)
# print(var)
