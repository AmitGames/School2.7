#   Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020
import os
import glob
import socket
import pyautogui
import subprocess
import glob
import shutil
import subprocess


IP = "localhost"
PORT = 6968


def receive_client_request(client_socket):
    """Receives the full message sent by the client

    Works with the protocol defined in the client's "send_request_to_server" function

    Returns:
        command: such as DIR, EXIT, SCREENSHOT etc
        params: the parameters of the command

    Example: 12DIR c:\cyber as input will result in command = 'DIR', params = 'c:\cyber'
    """
    length = client_socket.recv(1024).decode()
    data = client_socket.recv(int(length)).decode()
    try:
        command, params = data.split(' ', 1)
    except ValueError:
        command = data
        params = ''
    print(command, params)
    return command, params

def check_file_exists(file):
    return os.path.exists(file)
def check_file_copy_exists(params):
    org, dest = params.split('|', 1)
    if os.path.exists(org) and not os.path.exists(dest):
        return True
    else:
        return False

def check_client_request(command, params):
    """Check if the params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        error_msg: None if all is OK, otherwise some error message
    """
    error_msg = ''
    if command == "TAKE_SCREENSHOT":
        valid = True
    elif command == "DIR" and check_file_exists(params):
        valid = True
    elif command == "DELETE" and check_file_exists(params):
        valid = True
    elif command == "COPY" and check_file_copy_exists(params):
        valid = True
    elif command == "EXECUTE" and check_file_exists(params):
        valid = True
    elif command == "SEND_PHOTO" and check_file_exists(params):
        valid = True
    else:
        valid = False
        error_msg = f"ERROR THERE IS NO SUCH COMMAND AS {command} {params}"
    return valid, error_msg


def handle_client_request(command, params, socket):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory

    Returns:
        response: the requested data
    """
    if command == "TAKE_SCREENSHOT":
        data = take_screenshot(params)
    elif command == "DIR":
        data = dir(params)
    elif command == "DELETE":
        data = delete(params)
    elif command == "COPY":
        org, dest = params.split('|', 1)
        data = copy(org, dest)
    elif command == "EXECUTE":
        data = execute(params)
    elif command == "SEND_PHOTO":
        data = send_photo(params, socket)
    return data
'''====================commands========================='''
def take_screenshot(params):
    data = pyautogui.screenshot()
    data.save(params)
    return f"ScreenShot was saved at: {params}"

def dir(params):
    file_list = glob.glob(fr'{params}\*.*')
    data = ''
    for i in file_list:
        data += f"\n {i}"
    return data

def delete(params):
    os.remove(fr"{params}")
    return "The file was removed successfully"

def copy(org, dest):
    shutil.copy(fr"{org}", fr"{dest}")
    return "The file was copied successfully"

def execute(params):
    subprocess.call(fr"{params}")
    return "The process was successfully opened"

def send_photo(params, socket):
    data = socket.recv(1024).decode()
    if data == "start":
        f = open(params, 'rb')
        l = f.read(1024)
        while(l):
            socket.send(l)
            l = f.read(1024)
        f.close()
        return "The file was successfully sent"
    else:
        return "Time Out"
'''====================================================='''

def send_response_to_client(response, client_socket):
    """Create a protocol which sends the response to the client

    The protocol should be able to handle short responses as well as files
    (for example when needed to send the screenshot to the client)
    """
    client_socket.send(str(len(response)).encode())
    client_socket.send(response.encode())


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    client_socket, address = server_socket.accept()
    print("Got a connection from", address)

    # handle requests until user asks to exit
    done = False
    while not done:
        command, params = receive_client_request(client_socket)
        valid, error_msg = check_client_request(command, params)
        print(valid)
        client_socket.send(str(valid).encode())
        if valid:
            response = handle_client_request(command, params, client_socket)
            send_response_to_client(response, client_socket)
        elif command == 'EXIT':
            send_response_to_client("EXIT", client_socket)
            done = True
        else:
            send_response_to_client(error_msg, client_socket)

        

    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    main()