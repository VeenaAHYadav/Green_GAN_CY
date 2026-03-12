from scapy.all import *
import random
import time

target_ip = "192.168.29.155"

# discover MAC address
ans, unans = arping(target_ip)

print("Starting GAN-based port scan simulation...")

for port in range(1,200):

    packet = IP(dst=target_ip)/TCP(
        sport=random.randint(1024,65535),
        dport=port,
        flags="S"
    )

    send(packet, verbose=False)
    time.sleep(0.01)

print("GAN simulated port scan completed")