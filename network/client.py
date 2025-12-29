import socket
import threading

class ServerClient:
    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port
        self.sock = None
        self.on_command = None  # callback для обработки команд
        self.alive = True

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        threading.Thread(target=self._listen, daemon=True).start()

    def send(self, cmd: str):
        print("SEND:", cmd)
        if self.sock:
            try:
                self.sock.sendall((cmd + "\n").encode())
            except Exception as e:
                print("SEND ERROR:", e)

    def _listen(self):
        buffer = ""
        while self.alive:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                buffer += data.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if line and self.on_command:
                        print("RECV CMD:", line)
                        self.on_command(line)
            except Exception as e:
                print("LISTEN ERROR:", e)
                break

    def close(self):
        self.alive = False
        if self.sock:
            self.sock.close()
