import numpy as np
import math
import socket
import struct
import time
from tqdm import tqdm
from tkinter import messagebox as msgb
import tkinter as tk

wheel_radius = 3 / 100  # m
wheel_circumreference = 2 * math.pi * wheel_radius  # m
step_count = 200

def showMessage(message, type='info', timeout=2500):
    
    root = tk.Tk()
    root.withdraw()
    try:
        root.after(timeout, root.destroy)
        if type == 'info':
            msgb.showinfo('Info', message, master=root)
        elif type == 'warning':
            msgb.showwarning('Warning', message, master=root)
        elif type == 'error':
            msgb.showerror('Error', message, master=root)
    except:
        pass

def convert_to_step_counts(lin_speed_arr, ang_speed_arr, time_arr):
    left = []
    right = []

    # # convert to velocity
    # for i in range(len(time_arr)):
    #     left.append(lin_speed_arr[i] * 1000 / math.pi + ang_speed_arr[i] * 75 / math.pi)  # rpm
    #     right.append(lin_speed_arr[i] * 1000 / math.pi - ang_speed_arr[i] * 75 / math.pi)  # rpm

    # convert to velocity
    for i in range(len(time_arr)):
        left.append(1.5 * lin_speed_arr[i] + 1.3 * ang_speed_arr[i] * 15 / 200)  # m/s
        right.append(1.5 * lin_speed_arr[i] - 1.3 * ang_speed_arr[i] * 15 / 200)  # m/s

        # left.append(lin_speed_arr[i] + ang_speed_arr[i] * 15 / 200)  # m/s
        # right.append(lin_speed_arr[i] - ang_speed_arr[i] * 15 / 200)  # m/s

    print("after vel")
    print(f"time: {time_arr}")
    print(f"printing left: {left}")
    print(f"printing right: {right}")

    # convert to distance
    for i in range(len(time_arr) - 1):
        left[i] *= (time_arr[i+1] - time_arr[i]) / 1000  # m
        right[i] *= (time_arr[i+1] - time_arr[i]) / 1000  # m

    print("after dist")
    print(f"printing left: {left}")
    print(f"printing right: {right}")

    # convert to step count
    for i in range(len(time_arr) - 1):
        left[i] = left[i] / wheel_circumreference * step_count
        right[i] = right[i] / wheel_circumreference * step_count

    return left, right

def divide_list_into_chunks(lst, chunk_size):
    return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]

def send_array():

    time_arr = np.load("./time_arr.npy")
    lin_speed_arr = np.load("./lin_speed_arr.npy")
    ang_speed_arr = np.load("./ang_speed_arr.npy")

    l, r = convert_to_step_counts(lin_speed_arr, ang_speed_arr,time_arr)
    l = [int(x) for x in l]
    r = [int(x) for x in r]
    
    print("Time array length: " + str(len(time_arr)))
    print("Lin array length: " + str(len(l)))
    print("Ang array length: " + str(len(r)))

    # print("\n\n\n\n\n\n STEP COUNTS:")
    # print(f"printing linear: {lin_speed_arr}")
    # print(f"printing angular: {ang_speed_arr}")
    # print(f"time array: {time_arr}")

    l.append(-999)
    r.append(-999)

    time_arr = time_arr.tolist()
    time_arr.append(-999)

    print("\n\n\n\n\n\n STEP COUNTS:")
    print(f"printing left: {l}")
    print(f"printing right: {r}")
    print(f"time array: {time_arr}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("192.168.4.1", 333))
    socket_output_stream = sock.makefile('w')

    l = divide_list_into_chunks(l,100)
    r = divide_list_into_chunks(r,100)
    time_arr = divide_list_into_chunks(time_arr,100)

    showMessage("Left wheel data is sending!", timeout=1000)
    for chunk in l:
        byte_array_chunk_left = struct.pack('!' + str(len(chunk)) + 'f', *chunk)
        sock.sendall(byte_array_chunk_left)
        time.sleep(1)
    time.sleep(1)

    showMessage("Right wheel data is sending!", timeout=1000)
    for chunk in r:
        byte_array_chunk_right = struct.pack('!' + str(len(chunk)) + 'f', *chunk)
        sock.sendall(byte_array_chunk_right)
        time.sleep(1)
    time.sleep(1)

    showMessage("Time data is sending!", timeout=1000)
    for chunk in time_arr:
        byte_array_chunk_time = struct.pack('!' + str(len(chunk)) + 'f', *chunk)
        sock.sendall(byte_array_chunk_time)
        time.sleep(1)

    """
    print("sending left")
    for i in tqdm(range(len(l))):
        data_str = "{:.2f} ".format(l[i])
        #print(data_str)
        socket_output_stream.write(data_str)
        socket_output_stream.flush()
        time.sleep(0.2)
    #print("sending -999999")
    socket_output_stream.write("-999.99 ")
    socket_output_stream.flush()

    time.sleep(2)

    print("sending right")
    for i in tqdm(range(len(r))):
        data_str = "{:.2f} ".format(r[i])
        #print(data_str)
        socket_output_stream.write(data_str)
        socket_output_stream.flush()
        time.sleep(0.2)
    #print("sending -999999")
    socket_output_stream.write("-999.99 ")
    socket_output_stream.flush() 

    time.sleep(2)

    print("sending time")
    for i in tqdm(range(len(time_arr))):
        data_str = "{:.2f} ".format(time_arr[i])
        #print(data_str)
        socket_output_stream.write(data_str)
        socket_output_stream.flush()
        time.sleep(0.2)
    #print("sending -999999")
    socket_output_stream.write("-999.99 ")
    socket_output_stream.flush()
    """