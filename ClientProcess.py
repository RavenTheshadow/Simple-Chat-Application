import socket
import threading
import tkinter as tk
import time

class ChatApp:
    def __init__(self, title="My Simple Chat App", width=400, height=300, host='127.0.0.1', port=2000):
        self.MainWindow = self.create_window_frame(title, width, height)
        self.chat_list = self.create_chat_component()
        self.create_input_component()

        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
        threading.Thread(target=self.Connect_2_server, daemon=True, args=(host, port)).start()

    def Connect_2_server(self, host='127.0.0.1', port=2000):
        while True:
            try:
                self.Socket.connect((host, port))
                self.chat_list.insert(tk.END, f"Connecting to {host}:{port} successfully")
                threading.Thread(target=self.receive_messages, daemon=True).start()
                break
            except Exception as e:
                self.chat_list.insert(tk.END, f"Retrying connect to {host}:{port}")
                time.sleep(5)
    def receive_messages(self):
        while True:
            try:
                message = self.Socket.recv(1024).decode('utf-8')
                if message:
                    self.chat_list.insert(tk.END, f"Other: {message}")
                else:
                    break
            except Exception as e:
                self.chat_list.insert(tk.END, f"Error receiving message: {str(e)}")
                break

    def create_window_frame(self, title, width, height):
        window = tk.Tk()
        window.title(title)
        window.geometry(f"{width}x{height}")
        return window

    def create_chat_component(self):
        chat_frame = tk.Frame(self.MainWindow)
        chat_frame.pack(pady=5)

        chat_scroll = tk.Scrollbar(chat_frame)
        chat_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        chat_list = tk.Listbox(chat_frame, height=15, width=50, yscrollcommand=chat_scroll.set)
        chat_list.pack(side=tk.LEFT, fill=tk.BOTH)

        chat_scroll.config(command=chat_list.yview)
        return chat_list

    def create_input_component(self):
        input_frame = tk.Frame(self.MainWindow)
        input_frame.pack(pady=5)

        self.input_field = tk.Entry(input_frame, width=40)
        self.input_field.pack(side=tk.LEFT, padx=10)

        send_button = tk.Button(input_frame, text="Send", command=self.send_message)
        send_button.pack(side=tk.LEFT)

    def send_message(self):
        message = self.input_field.get()
        if message:
            self.chat_list.insert(tk.END, f"Me: {message}")
            self.input_field.delete(0, tk.END)
            try:
                self.Socket.send(message.encode('utf-8'))
            except Exception as e:
                self.chat_list.insert(tk.END, f"Error sending message: {str(e)}")

    def process(self):
        self.MainWindow.mainloop()
