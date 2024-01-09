import socket
import threading

class Server:
    def __init__(self):
        self.data = []
        self.names = []
        self.accepting_connections = True
        self.connections = []
        self.connected = False
    def connect(self, addr):
        self.sock = socket.create_connection(addr)
        self.connected = True

    def sync(self, name, value):
        if self.connected:
            self.sock.send(f"C {name} {value}".encode())
            msg = self.sock.recv(1024).decode()
        else:
            self.data.append(value)
            self.names.append(name)

    def get(self, name):
        if self.connected:
            self.sock.send(f"G {name} 0".encode())
            msg = self.sock.recv(1024).decode()
            return msg
        else:
            return self.data[self.names.index(name)]

    def set(self, name, value):

        if self.connected:
            self.sock.send(f"S {name} {value}".encode())
            msg = self.sock.recv(1024).decode()
        else:
            self.data[self.names.index(name)] = value
    def disconnect(self):
        self.sock.send(b"D 0 0")


    def serve(self, addr):
        if not self.connected:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(addr)
            self.sock.listen()

            def handle_connection(conn, addr):
                print(f'{addr} has connected')
                self.connections.append(conn)
                connected = True
                while connected:
                    msg_raw = conn.recv(1096)
                    if msg_raw:
                        msg = msg_raw.decode()
                        verb = msg.split(' ')[0]
                        name = msg.split(' ')[1]
                        value = msg.split(' ')[2]
                        if verb == 'S':
                            self.data[self.names.index(name)] = value
                            conn.send(b"OK")
                        elif verb == 'G':
                            conn.send(self.data[self.names.index(name)].encode())
                        elif verb == 'C':
                            self.data.append(value)
                            self.names.append(name)
                            conn.send(b"OK")
                        elif verb == 'D':
                            self.connections.remove(conn)
                            conn.close()
                            connected = False


            print("Waiting for connections...")
            while self.accepting_connections:
                c, a = self.sock.accept()
                threading.Thread(target=handle_connection, args=(c, a)).start()

        else:
            raise ConnectionError("You cannot start a server from a client.")