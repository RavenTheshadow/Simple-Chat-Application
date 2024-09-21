import socket
import threading
import tkinter as tk

def get_IP():
    Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        Socket.connect(('8.8.8.8', 1))
        IP = Socket.getsockname()[0]
    except Exception as e:
        print(f"Error getting IP address: {e}")
        IP = '127.0.0.1'
    finally:
        Socket.close()
        return IP

class Server_Process:
    def __init__(self, host='127.0.0.1', port=2000):
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.bind((host, port))
        self.Socket.listen(5)
        print(f"Server started at {host}:{port}")

    def New_Connection(self, obj, addr, chat_app):
        print(f"A new connection from {addr}")
        while True:
            try:
                message = obj.recv(1024).decode('utf-8')
                chat_app.chat_list.insert(tk.END, f"Client: {message}")
                if not message:
                    print(f"Connection closed by {addr}")
                    break
            except Exception as e:
                print(f"Error receiving message from {addr}: {e}")
                break
        obj.close()

    def Server_Process(self, chat_app):
        while True:
            obj, addr = self.Socket.accept()
            new_connection_thread = threading.Thread(target=self.New_Connection, args=(obj, addr, chat_app))
            new_connection_thread.start()