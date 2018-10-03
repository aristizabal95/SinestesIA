import os
import threading
import socket

import global_vars

def pdreceive():
    HOST = 'localhost'
    PORT = 6000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print("Connected by", addr)
    while True:
        data = conn.recv(2048)
        string = data.decode('utf-8')
        string = string.replace(';\n','') # Remove the semicolon at the end of the string
        string_list = string.split(" ") # transform the string into an array
        global_vars.g_current_state = list(map(float, string_list)) # transform the list of strings to ints
<<<<<<< HEAD
        # print(global_vars.g_current_state)
=======
        print(global_vars.g_current_state)
>>>>>>> 8fa155ab4f7676c670900b6d3a78c9cb228fa98e

def send2Pd(message=''):
    os.system("echo '" + message + "' | pdsend 3000")

def stream_data(action_arr):
    for action in action_arr:
        msg = ' '.join(map(str,action)) + ';'
        send2Pd(msg)
