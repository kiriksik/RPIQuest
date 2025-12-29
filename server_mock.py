import socket
import threading

clients = []

def handle_client(conn, addr):
    print(f"Client connected: {addr}")
    clients.append(conn)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode().strip()
            print("RECV FROM CLIENT:", msg)
    finally:
        clients.remove(conn)
        conn.close()
        print(f"Client disconnected: {addr}")

def start_server(host="localhost", port=8000):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    print(f"Server listening on {host}:{port}")

    def accept_loop():
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

    threading.Thread(target=accept_loop, daemon=True).start()
    return s

def send_to_clients(cmd):
    for c in clients:
        try:
            c.sendall((cmd + "\n").encode())
        except:
            pass

if __name__ == "__main__":
    server = start_server()

    print("Type commands to send to client. Example: startPC, reset, passPC, passProjector, exit")
    while True:
        cmd = input("SEND CMD > ")
        send_to_clients(cmd)
