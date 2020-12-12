#   Ex. 2.7 template - protocol


LENGTH_FIELD_SIZE = 4
PORT = 6968


'''def check_cmd(command):
    r"""
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """

    if "TAKE_SCREENSHOT" in command:
        valid = True
    elif command == "DIR" in command:
        valid = True
    elif command == "DELETE" in command:
        valid = True
    elif command == "COPY" in command:
        valid = True
    elif command == "EXECUTE":
        valid = True
    elif command == "SEND_PHOTO":
        valid = True
    elif command == "EXIT":
        valid = True
    else:
        valid = False

    return valid'''


def send_msg(socket, data):
    """
    Create a valid protocol message, with length field
    """
    socket.send(str(len(data)).encode())
    socket.send(data.encode())
    print("The message has been sent")






"""def get_msg(my_socket):
    
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    

    # (5)
    return True, "OK"""


