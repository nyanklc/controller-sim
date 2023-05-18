import numpy as np
import math
import serial

time_arr = np.load("./time_arr.npy")
lin_speed_arr = np.load("./lin_speed_arr.npy")
ang_speed_arr = np.load("./ang_speed_arr.npy")

def convert_to_motor_rpm(lin, ang):
    left = []
    right = []

    for i in range(len(time_arr)):
        left.append(lin_speed_arr[i] / 3.6 / math.pi + ang_speed_arr[i] * 2.5 / 2 / math.pi * 60)
        right.append(lin_speed_arr[i] / 3.6 / math.pi - ang_speed_arr[i] * 2.5 / 2 / math.pi * 60)

    return left, right

l, r = convert_to_motor_rpm(lin_speed_arr, ang_speed_arr)
print(l)
print("\n\n\n\n\n\n\n\n")
print(r)

print(f"EEEEEEEEEEEEEEEEEEEEEEEEEE {len(l)}")
print(f"DDDDDDDDDDDDDDDDDDDDDDDDDD {len(r)}")
print(f"DDDDDDDDDDDDDDDDDDDDDDDDDD {len(time_arr)}")

import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.4.1", 333))
socket_output_stream = sock.makefile('w')

print("sending left")
for i in range(len(l)):
    data_str = "{:.2f} ".format(l[i])
    print(data_str)
    socket_output_stream.write(data_str)
    socket_output_stream.flush()
    time.sleep(0.2)
print("sending -999999")
socket_output_stream.write("-999.99 ")
socket_output_stream.flush()

time.sleep(2)

print("sending right")
for i in range(len(r)):
    data_str = "{:.2f} ".format(r[i])
    print(data_str)
    socket_output_stream.write(data_str)
    socket_output_stream.flush()
    time.sleep(0.2)
print("sending -999999")
socket_output_stream.write("-999.99 ")
socket_output_stream.flush() 

time.sleep(2)

print("sending time")
for i in range(len(time_arr)):
    data_str = "{:.2f} ".format(time_arr[i])
    print(data_str)
    socket_output_stream.write(data_str)
    socket_output_stream.flush()
    time.sleep(0.2)
print("sending -999999")
socket_output_stream.write("-999.99 ")
socket_output_stream.flush()