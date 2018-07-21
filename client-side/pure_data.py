import os
import threading
import socket

import global_vars

def pdreceive():
    HOST = ''
    PORT = 6000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print("Connected by", addr)
    while True:
        data = conn.recv(1024)
        string = data.decode('utf-8')
        string = string.replace(';\n','') # Remove the semicolon at the end of the string
        string_list = string.split(" ") # transform the string into an array
        global_vars.g_current_state = list(map(int, string_list)) # transform the list of strings to ints



def send2Pd(message=''):
    os.system("echo '" + message + "' | pdsend 3000")
