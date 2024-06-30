import socket
import threading

class Server:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connections = {}

    def start(self):
        try:
            with self.server_socket as s:
                s.bind((self.host, self.port))
                s.listen()
                print(f"Server is listening on {self.host}:{self.port}")

                while True:
                    conn, addr = s.accept()
                    client_thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                    client_thread.start()
        except OSError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("Server interrupted. Closing connections.")
            self.close_connections()

    def server_recv(self, server_socket, ip):
        while True:
            try:
                data = server_socket.recv(1024).decode("utf-8").strip()
                if not data:
                    break
                print(data)
            except ConnectionResetError:
                break

        del self.client_connections[ip]
        print(f"Client {ip} disconnected")
        server_socket.close()

    def handle_client(self, server_socket, addr):
        ip = addr[0]
        print(f'Connected to {addr}')
        self.client_connections[ip] = server_socket
        threading.Thread(target=self.server_recv, args=(server_socket, ip), daemon=True).start()

    def server_input(self):
        while True:
            command = input("Enter server msg:")
            for client_socket in self.client_connections.values():
                try:
                    client_socket.send(command.encode())
                except ConnectionError:
                    # Handle cases where the client disconnected
                    pass

    def close_connections(self):
        for client_socket in self.client_connections.values():
            client_socket.close()

if __name__ == "__main__":
    server = Server()

    # Start a thread for receiving messages
    threading.Thread(target=server.server_input).start()
    server.start()
