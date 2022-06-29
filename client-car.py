#!/usr/bin/python3           # This is client.py file

import socket
from picarx import Picarx
import time

PORT = 9999

def linetrack(px_power):
  try:
    px = Picarx()
    # px = Picarx(grayscale_pins=['A0', 'A1', 'A2']) 

    while True:
        gm_val_list = px.get_grayscale_data()
        print("gm_val_list:",gm_val_list)
        gm_status = px.get_line_status(gm_val_list)
        print("gm_status:",gm_status)

        if gm_status == 'forward':
            print(1)
            px.forward(px_power) 

        elif gm_status == 'left':
            px.set_dir_servo_angle(12)
            px.forward(px_power) 

        elif gm_status == 'right':
            px.set_dir_servo_angle(-12)
            px.forward(px_power) 
        else:
            px.set_dir_servo_angle(0)
            px.stop()
  finally:
      px.stop()

def main():

    
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # get local machine name
    host = '10.64.11.2'
    
    # connection to hostname on the port.
    s.connect((host, PORT))

    # Receive no more than 1024 bytes
    msg = s.recv(1024)
    
    print (msg.decode('ascii'))

    try: 
        px = Picarx()
        px_power = 10

        while True:
            msg = s.recv(1024)
            command = msg.decode('ascii')
            print (command)

            if command.startswith('f '):
                cmd_split = command.split(' ')
                if len(cmd_split) == 2:
                    duration = cmd_split[1]

                    px.forward(px_power)
                    time.sleep(int(duration))
                    px.stop()

            elif command.startswith('b '):
                cmd_split = command.split(' ')
                if len(cmd_split) == 2:
                    duration = cmd_split[1]

                    px.backward(px_power)
                    time.sleep(int(duration))
                    px.stop()

            elif command == 'linetrack':
                linetrack()

            elif command.startswith('speed '):
                cmd_split = command.split(' ')
                if len(cmd_split) == 2:
                    px_power = int(cmd_split[1])
            elif command == 'exit':
                s.close()
                break
            else:
                print ("Unrecognized command. Do nothing.\n")
    finally:
        s.close()

    s.close()

if __name__ == '__main__':
    main()
