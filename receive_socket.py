'''
Author: wakaba blues243134@gmail.com
Date: 2024-03-06 15:33:21
LastEditors: wakaba blues243134@gmail.com
LastEditTime: 2024-03-06 21:25:43
FilePath: /unified_process/receive_socket.py
Description: 

Copyright (c) 2024 by wakaba All Rights Reserved. 
'''

import socket

HOST = '0.0.0.0'  # 监听所有接口
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print("Waiting for connection...")
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('Received from phone:', data.decode())