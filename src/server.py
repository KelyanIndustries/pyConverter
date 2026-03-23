import socket
import threading
import queue
from .config import HOST, PORT

file_queue = queue.Queue()

def send_file_to_server(file_path):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(file_path.encode('utf-8'))
    except Exception:
        pass

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
    except OSError:
        return False

    def listen():
        while True:
            try:
                conn, addr = server_socket.accept()
                with conn:
                    data = conn.recv(4096)
                    if data:
                        file_path = data.decode('utf-8')
                        file_queue.put(file_path)
            except Exception:
                break
    
    thread = threading.Thread(target=listen, daemon=True)
    thread.start()
    return True
