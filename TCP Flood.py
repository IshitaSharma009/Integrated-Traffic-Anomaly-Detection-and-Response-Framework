import socket

def tcp_attack(target_ip, target_port, message, num_requests):
  try:
      for _ in range(num_requests):
          # Create a socket object
          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
              # Connect to the server
              s.connect((target_ip, target_port))
              # Send data
              s.sendall(message.encode())
              # Receive response (optional)
              response = s.recv(1024)
              print(f"Received: {response.decode()}")
  except Exception as e:
      print(f"An error occurred: {e}")

if __name__ == "__main__":
  target_ip = "127.0.0.1"
  target_port = 7612
  message = "Hello, Server!"
  num_requests = 10  # Number of requests to send

  tcp_attack(target_ip, target_port, message,num_requests)
