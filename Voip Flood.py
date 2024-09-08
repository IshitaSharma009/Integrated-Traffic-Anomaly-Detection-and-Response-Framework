import socket
import struct
import time
import random

# RTP packet construction (simplified for simulation)
def create_rtp_packet(sequence_number, timestamp, payload_type=0, ssrc=12345):
    version = 2        # RTP version
    padding = 0        # No padding
    extension = 0      # No extension
    csrc_count = 0     # No CSRC
    marker = 0         # Marker bit
    payload_type = payload_type  # Payload type (0 is for PCM audio)
    
    # First byte (V=2, P=0, X=0, CC=0)
    first_byte = (version << 6) | (padding << 5) | (extension << 4) | csrc_count
    
    # Second byte (M=0, PT=payload_type)
    second_byte = (marker << 7) | payload_type
    
    # Pack the RTP header fields into a byte sequence
    rtp_header = struct.pack('!BBHII', first_byte, second_byte, sequence_number, timestamp, ssrc)
    
    # Simulated payload (e.g., 160 bytes of audio)
    payload = bytes(random.getrandbits(8) for _ in range(160))
    
    return rtp_header + payload

def send_voip_packet(target_ip, target_port, num_packets, delay):
    try:
        # Create a UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Initial sequence number and timestamp
        sequence_number = 0
        timestamp = 0
        
        for _ in range(num_packets):
            # Create RTP packet
            rtp_packet = create_rtp_packet(sequence_number, timestamp)
            
            # Send the packet over UDP
            udp_socket.sendto(rtp_packet, (target_ip, target_port))
            print(f"Sent RTP packet {sequence_number} to {target_ip}:{target_port}")
            
            # Increment the sequence number and timestamp for the next packet
            sequence_number += 1
            timestamp += 160  # Typically, one packet corresponds to 20ms of audio, adjust accordingly
            
            # Wait before sending the next packet
            time.sleep(delay)

    except socket.error as e:
        print(f"An error occurred: {e}")
    finally:
        udp_socket.close()

def main():
    # Take the target IP address and port
    target_ip = input("Enter the target IP address (e.g., 192.168.1.1): ")
    target_port = int(input("Enter the target port (e.g., 5060 for SIP or 5004 for RTP): "))
    
    # Number of packets and delay between them
    num_packets = int(input("Enter the number of RTP packets to send: "))
    delay = float(input("Enter the delay between packets (in seconds, 0 for no delay): "))

    # Send VoIP (RTP) packets
    send_voip_packet(target_ip, target_port, num_packets, delay)

if __name__ == "__main__":
    main()
