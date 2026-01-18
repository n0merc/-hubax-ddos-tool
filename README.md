# HUBaxDDOS v2.0 - Maximum Power Network Stress Testing Tool

HUBaxDDOS is a powerful, Python-based network security tool designed for stress testing and analyzing network resilience. This version is specifically optimized to bypass common protections like Cloudflare and handle HTTPS (SSL) targets using high-speed multi-threading and IP spoofing techniques.

##  Key Features

* **MAX HTTPS/SSL Flood:** Performs high-frequency GET requests over Port 443 with full SSL/TLS handshake support.
* **IP Spoofing:** Randomizes `X-Forwarded-For` and `X-Real-IP` headers to mask the origin IP and mimic traffic from multiple global sources.
* **User-Agent Rotation:** Automatically switches between various modern browser strings (Chrome, Safari, iOS) to avoid signature-based detection.
* **Keep-Alive Pipelining:** Sends multiple requests through a single persistent connection to maximize Requests Per Second (RPS).
* **UDP Flood:** Floods targets with large, randomized packets to test bandwidth capacity.
* **Real-time Statistics:** Track the total number of packets/requests sent during an active session.

## 🛠 Installation

1.  Ensure you have **Python 3.x** installed on your system.
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

##  Usage

Run the tool using the following command:
```bash
python3 hubaxddos.py
Commands:
https: Launch a high-power HTTPS attack (Optimized for websites).

udp: Launch a UDP packet flood (Optimized for IP/Port stress).

stats: View current session statistics.

stop: Kill all active attack threads.

exit: Close the application.

 Optimization (Linux/Mac)
To handle thousands of concurrent threads and avoid "Too many open files" errors, increase your system's descriptor limit before running the script:

Bash

ulimit -n 10000

```

Disclaimer

This tool is provided for educational purposes and authorized security testing only. Using this tool to attack infrastructure without prior mutual consent is illegal. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.
