#!/usr/bin/python3           # This is client.py file

import socket
import argparse
from picarx import Picarx
import time

PORT = 9999

def is_time_up(end):
    now = time.time()
    return True if end < now else False


def linetrack(px_power=10, duration=0):
  try:
    px = Picarx()
    # px = Picarx(grayscale_pins=['A0', 'A1', 'A2'])

    start = time.time()
    end = start + duration 

    while True:
        gm_val_list = px.get_grayscale_data()
        print("gm_val_list:",gm_val_list)
        gm_status = px.get_line_status(gm_val_list)
        print("gm_status:",gm_status)

        if gm_status == 'forward':
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

        # Check if time is up.
        # If duration is 0, that means go on forever until end of tape is detected.
        # So, only check if duration is not zero.
        if duration != 0 and is_time_up(end):
            break

  finally:
      px.stop()


def main():
    
    parser = argparse.ArgumentParser(description='Script for running PiCarX client')
    parser.add_argument('-d', dest='dest_ip', action='store', required=True,
            help='Destination IP address (numerical)')

    # Parse
    args = parser.parse_args()

    # get local machine name
    host = args.dest_ip

    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
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
                    px.forward(0)

            elif command.startswith('b '):
                cmd_split = command.split(' ')
                if len(cmd_split) == 2:
                    duration = cmd_split[1]

                    px.backward(px_power)
                    time.sleep(int(duration))
                    px.forward(0)

            elif command.startswith('linetrack '):
                cmd_split = command.split(' ')
                if len(cmd_split) == 2:
                    duration = cmd_split[1]

                    linetrack(px_power=px_power)
                    time.sleep(int(duration))
                    px.forward(0)

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
