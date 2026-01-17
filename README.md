# -hubax-ddos-tool
# Install dependencies
pip3 install requests

# Run the tool (needs root for SYN flood)
sudo python3 hubax_ddos.py <target_ip> <port> <threads> <duration>

# Example:
sudo python3 hubax_ddos.py 192.168.1.100 80 1000 300
```

## GitHub README Template:

```markdown
# HUBAX DDoS Tool

**Disclaimer: This tool is for educational purposes and authorized penetration testing only. Unauthorized use is illegal.**

## Features
- Multi-vector DDoS attacks
- HTTP/S flood
- SYN flood (requires root)
- UDP flood
- Slowloris attack
- IP spoofing
- Configurable threads and duration

## Installation
```bash
git clone https://github.com/yourusername/hubax-ddos-tool.git
cd hubax-ddos-tool
pip3 install -r requirements.txt
```

## Usage
```bash
python3 hubax_ddos.py <target_ip> [port] [threads] [duration]
```

## Legal Warning
Only use on systems you own or have explicit permission to test.

## License
MIT License
