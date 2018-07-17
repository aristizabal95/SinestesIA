import os
import threading
import socket

current_state = []

def pdreceive():
    global current_state
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
        current_state = list(map(int, string_list)) # transform the list of strings to ints
        print(current_state)



def send2Pd(message=''):
    os.system("echo '" + message + "' | pdsend 3000")
