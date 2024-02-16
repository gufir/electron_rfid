from serial import Serial

READ_EPC = 'BB 00 39 00 09 00 00 00 00 01 00 00 00 0A 4D 7E'
INVENTORY = 'BB 00 22 00 00 22 7E' #Single Inventory
INVENTORY2 = 'BB 00 27 00 03 22 27 10 83 7E' #MULTIPLE Inventory
VERSION = 'BB 00 03 00 01 00 04 7E'

test_serial = Serial('COM4', 115200, timeout=0.1)

def send_cmd(cmd):
    data = bytes.fromhex(cmd)
    test_serial.write(data)
    response = test_serial.read(512)
    response_hex = response.hex().upper()
    hex_list = [response_hex[i:i+2] for i in range(0, len(response_hex), 2)]
    hex_space = ' '.join(hex_list)
    
    return hex_space

def read_EPC():
    return send_cmd(READ_EPC)

def single():
    return send_cmd(INVENTORY)

def multiple():
    return send_cmd(INVENTORY2)

def version():
    return send_cmd(VERSION)





