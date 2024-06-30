import socket, threading
import time

class Client:
    def __init__(self, server_ip, server_port=12345):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            print(f"Connected to server at {self.server_ip}:{self.server_port}")
        except: pass
    def client_send(self, data):
        self.client_socket.sendall(data.encode())
    
    def client_recv(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode("utf-8").strip()
                print(data)
            except ConnectionResetError:
                break

if __name__ == "__main__":
    client = Client()
    client.connect()
    client_send_thread = threading.Thread(target=client.client_send)
    client_send_thread.start()
    client.client_recv()
