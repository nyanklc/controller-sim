points = [(0, 10), (0, 20), (20, 20), (30, 20)]

import socket
import time

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("192.168.4.1", 333))
    socket_output_stream = sock.makefile('w')

    for i in range(len(points)):
        data_str = "{:.2f} {:.2f}".format(points[i][0], points[i][1])
        print(data_str)
        socket_output_stream.write(data_str)
        socket_output_stream.flush()
        time.sleep(0.1)
    socket_output_stream.write("-999.99 -999.99")
    socket_output_stream.flush()
    while True:
        pass