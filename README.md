# HUBaxDDOS - Advanced Network Stress Testing Tool

##  DISCLAIMER
**This tool is for EDUCATIONAL PURPOSES ONLY. Use only on systems you own or have explicit permission to test. Unauthorized use is illegal and can result in severe penalties.**

##  Features
- Multiple attack vectors (TCP, UDP, HTTP, SYN, ICMP, Slowloris, DNS)
- Multi-threaded architecture
- Real-time statistics
- Interactive menu system
- Professional logging
- Easy to use interface

## Installation
```bash
git clone https://github.com/anujin696969/hubaxddos.git
cd hubaxddos
# No installation required - pure Python
```

##  Usage
### Interactive Mode:
```bash
python3 hubaxddos.py -i
```

### Command Line:
```bash
# TCP Flood
python3 hubaxddos.py -t 192.168.1.1 -p 80 -m tcp -th 500 -d 60

# UDP Flood
python3 hubaxddos.py -t 192.168.1.1 -p 53 -m udp -th 1000 -d 120

# HTTP Flood
python3 hubaxddos.py -t https://target.com -m http -th 300 -d 180
```

##  Menu Options
```
[1] TCP Flood Attack      - Standard TCP connection flood
[2] UDP Flood Attack      - Connectionless UDP flood
[3] HTTP Flood Attack     - Layer 7 HTTP request flood
[4] SYN Flood Attack      - Half-open connection attack
[5] ICMP Flood Attack     - Ping flood attack
[6] Slowloris Attack      - Slow HTTP headers attack
[7] DNS Amplification     - DNS reflection attack
[8] Multi-Vector Attack   - Combine multiple methods
[9] Show Statistics       - Display attack stats
[10] Stop All Attacks     - Stop all running attacks
[11] Help                 - Show help menu
[12] Exit                 - Exit the program
```

##  Configuration
Edit the constants at the top of `hubaxddos.py`:
```python
MAX_THREADS = 1000      # Maximum concurrent threads
PACKET_SIZE = 4096      # Size of each packet
TIMEOUT = 3             # Socket timeout in seconds
ATTACK_DURATION = 300   # Default attack duration
```

##  Statistics
The tool provides real-time statistics including:
- Target information
- Attack duration
- Packets sent
- Bytes transferred
- Packets per second
- Current status

##  Legal Notice
This software is provided "as is" without warranty of any kind. The author is not responsible for any misuse or damage caused by this program. Users assume full responsibility for their actions.

##  Contributing
Contributions are welcome! Please read the contributing guidelines before submitting pull requests.

## 📄 License
MIT License - See LICENSE file for details.

## 💬 Support
For questions or issues, please open an issue on GitHub.
