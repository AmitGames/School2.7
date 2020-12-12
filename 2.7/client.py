#   Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020


import socket
import glob
import os


IP = 'localhost'
SAVED_PHOTO_LOCATION = 'C:\photo\lol.png' # The path + filename where the copy of the screenshot at the client should be saved
PORT = 6968


def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    if("SEND_PHOTO" in cmd):
        print("start")
        my_socket.send("start".encode())
        
        f = open(f'{SAVED_PHOTO_LOCATION}', 'wb')
        l = my_socket.recv(1024)
        while(l):
            f.write(l)
            l = my_socket.recv(1024)
        f.close()
        print("done!")
        length = my_socket.recv(1024).decode()
        data = my_socket.recv(int(length)).decode()
        return data
    else:
        print("lol")
        length = my_socket.recv(1024).decode()
        data = my_socket.recv(int(length)).decode()
        return data
    

def send_msg(socket, data):
    """
    Create a valid protocol message, with length field
    """
    socket.send(str(len(data)).encode())
    socket.send(data.encode())
    print("The message has been sent...")


def main():
    # open socket with the server

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, PORT))

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    RUN = True
    while RUN:
        cmd = input("Please enter command:\n")
        send_msg(my_socket, cmd)
        data = my_socket.recv(1024).decode()
        if data == "True":
            d = handle_server_response(my_socket, cmd)
            print(d)
        elif data == 'False':
            print(handle_server_response(my_socket, cmd))
        if cmd == 'EXIT':
            RUN = False
    my_socket.close()

if __name__ == '__main__':
    main()