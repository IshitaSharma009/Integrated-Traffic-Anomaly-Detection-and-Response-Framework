import pyshark
import logging
import time
import smtplib
from email.mime.text import MIMEText
import matplotlib.pyplot as plt
import hashlib

# Initialize logging for anomaly detection
logging.basicConfig(filename='traffic_anomalies.log', level=logging.INFO)

# Traffic stats and priority mapping
traffic_stats = {'HTTP': 0, 'VoIP': 0, 'TCP': 0, 'UDP': 0, 'Other': 0}
traffic_counts = {'HTTP': [], 'VoIP': [], 'TCP': [], 'UDP': [], 'Other': []}
time_intervals = []
priority = {'VoIP': 1, 'HTTP': 2, 'TCP': 3, 'UDP': 3}

# Define thresholds for detecting anomalies
normal_thresholds = {'HTTP': 50, 'TCP': 150, 'UDP': 80, 'Other': 50}

# Hash function to anonymize IP addresses
def hash_ip(ip_address):
    return hashlib.sha256(ip_address.encode()).hexdigest()

# Function to classify packets properly using pyshark layers
def classify_packet(packet):
    try:
        if hasattr(packet, 'http'):  # HTTP protocol
            traffic_stats['HTTP'] += 1
        elif hasattr(packet, 'rtp') or hasattr(packet, 'sip'):  # VoIP protocols
            traffic_stats['VoIP'] += 1
        elif hasattr(packet, 'tcp'):  # TCP protocol
            traffic_stats['TCP'] += 1
        elif hasattr(packet, 'udp'):  # UDP protocol
            traffic_stats['UDP'] += 1
        else:  # Other protocols
            traffic_stats['Other'] += 1
    except AttributeError:
        pass

# Function to detect anomalies
def detect_anomaly():
    anomalies = []
    for protocol, count in traffic_stats.items():
        if protocol in normal_thresholds and count > normal_thresholds[protocol]:
            anomalies.append(f"Anomaly detected in {protocol} traffic: {count} packets")
    return anomalies

# Function to log detected anomalies
def log_anomaly(anomalies):
    for anomaly in anomalies:
        logging.info(anomaly)

# Function to send email alerts for detected anomalies
def send_alert(anomaly):
    msg = MIMEText(anomaly)
    msg['Subject'] = 'Network Anomaly Detected'
    msg['From'] = 'xxxx@gmail.com'
    msg['To'] = 'xxxx@gmail.com'

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login("xxxx@gmail.com", "xxxx")
            server.sendmail("xxxxx@gmail.com", "xxxx@gmail.com", msg.as_string())
    except Exception as e:
        print(f"Failed to send email alert: {e}")

# Function to prioritize traffic based on the type
def prioritize_traffic():
    if traffic_stats['VoIP'] > 0:
        print("VoIP traffic detected. Prioritizing VoIP.")
    elif traffic_stats['HTTP'] > 0:
        print("HTTP traffic detected. Medium priority.")
    else:
        print("Other traffic. Low priority.")

# Function to update real-time plot
def update_plot():
    plt.clf()
    for protocol in traffic_counts:
        plt.plot(time_intervals, traffic_counts[protocol], label=protocol)
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Packet Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.draw()
    plt.pause(0.1)

# Function to generate traffic report and ensure it's updated
def generate_report():
    with open("traffic_report.txt", "w") as f:
        f.write(f"Traffic Report:\n")
        for protocol, count in traffic_stats.items():
            f.write(f"{protocol} Packets: {count}\n")

        anomalies = detect_anomaly()
        if anomalies:
            f.write("Anomalies Detected:\n")
            for anomaly in anomalies:
                f.write(f"- {anomaly}\n")

# Function to simulate dropping packets
def mitigate_attack(packet):
    anomalies = detect_anomaly()
    if anomalies:
        print("Suspicious traffic detected. Dropping packet.")
        return True  # Simulating packet drop
    return False  # Continue processing packet

def main():
    # Enable interactive mode for matplotlib
    plt.ion()

    # Real-time packet capture and processing
    capture = pyshark.LiveCapture(interface='Wi-Fi 2')

    try:
        # Simulate real-time packet capture and traffic analysis over 100 intervals
        for i in range(100):
            packets = capture.sniff_continuously(packet_count=10)
            for packet in packets:
                if mitigate_attack(packet):  # Skip processing if anomaly detected
                    continue
                
                try:
                    classify_packet(packet)
                except Exception as e:
                    print(f"Error processing packet: {e}")

            # Update time intervals and traffic counts
            time_intervals.append(i)
            for key in traffic_counts:
                traffic_counts[key].append(traffic_stats[key])

            # Check for anomalies and log if found
            anomalies = detect_anomaly()
            if anomalies:
                log_anomaly(anomalies)
                for anomaly in anomalies:
                    send_alert(anomaly)

            # Prioritize traffic based on traffic stats
            prioritize_traffic()

            # Update real-time plot
            update_plot()

            # Generate report after each interval to ensure updates
            generate_report()

            time.sleep(1)  # Simulate real-time packet capture delay

    except KeyboardInterrupt:
        print("Capture stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        capture.close()
        # Generate the final traffic report
        generate_report()
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    main()
