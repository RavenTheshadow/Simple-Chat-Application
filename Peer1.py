from ClientProcess import ChatApp
from ServerProcess import Server_Process, get_IP
import threading



def create_UI(my_IP):
    chat_app = ChatApp("Peer 1 Chat App", host=my_IP, port= 4000)
    threading.Thread(target=Server_Process_Handler, daemon=True, args=(chat_app, my_IP)).start()
    chat_app.process()


def Server_Process_Handler(chat_app, my_IP):
    my_port = 7777
    server = Server_Process(my_IP, my_port)
    server.Server_Process(chat_app)


if __name__ == '__main__':
    my_IP = get_IP()
    create_UI(my_IP)
    print("Program terminated")