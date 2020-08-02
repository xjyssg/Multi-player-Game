import socket
import msvcrt
import threading
from queue import Queue
from utils import Request_Message
from utils import Response_Message


class Keyboard:
    def __init__(self):
        valid_button = ['W', 'A', 'S', 'D','K','/','#']
        self.valid_button = valid_button
        self.enabled = True

    def read(self, button_queue):
        while (self.enabled):
            if msvcrt.kbhit():
                button = chr(ord(msvcrt.getch())).upper()
                if (button in self.valid_button):
                    button_queue.put(button)
                    if (button == '/'):
                        self.enabled = False
                


class Client:
    def __init__(self, server_IP, server_TCP_port, server_UDP_port, socket_type):
        self.has_socket = False
        self.server_IP = server_IP
        self.server_TCP_port = server_TCP_port
        self.server_UDP_port = server_UDP_port
        self.socket_type = socket_type
        
    def connect_server(self):
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if (self.socket_type == "TCP"):
            new_socket.connect((self.server_IP, self.server_TCP_port))
        self.socket = new_socket
        self.has_socket = True

    def disconnect_server(self):
        self.socket.close()
        self.has_socket = False

    def send_msg(self, send_queue):
        while (self.has_socket):
            if not send_queue.empty():
                encoded_msg = send_queue.get()
                if (self.socket_type == "TCP"):
                    self.socket.send(encoded_msg)
                else:
                    self.socket.sendto(encoded_msg, (self.server_IP, self.server_UDP_port))

    def receive_msg(self, receive_queue):
        while (self.has_socket):
            if (self.socket_type == "TCP"):
                encoded_msg = self.socket.recv(1024)
            else:
                encoded_msg = self.socket.recvfrom(1024)
            receive_queue.put(encoded_msg)




class Player:
    def __init__(self, account, server_IP, server_TCP_port, server_UDP_port, socket_type):
        self.account = account
        self.valid = True

        button_queue = Queue()
        self.button_queue = button_queue
        send_queue = Queue()
        self.send_queue = send_queue
        receive_queue = Queue()
        self.receive_queue = receive_queue

        self.keyboard = Keyboard()
        self.Request = Request_Message()
        self.Response = Response_Message()
        self.server_IP = server_IP
        self.server_TCP_port = server_TCP_port
        self.server_UDP_port = server_UDP_port
        self.socket_type = socket_type
        self.network = Client(server_IP, server_TCP_port, server_UDP_port, socket_type)

    def process_sending(self):
        while (self.valid):
            if (not self.button_queue.empty()):
                button = self.button_queue.get()
                content = self.account + ':' + button
                msg = self.Request.generate_message("POST", content)
                self.send_queue.put(msg)

    def start_send(self):
        read_button = threading.Thread(target=self.keyboard.read, args=(self.button_queue,))
        read_button.start()

        self.network.connect_server()
        process = threading.Thread(target=self.process_sending)
        process.start()

        send = threading.Thread(target=self.network.send_msg, args=(self.send_queue,))
        send.start()

    def process_receiving(self):
        while (self.valid):
            if (not self.receive_queue.empty()):
                encoded_msg = self.receive_queue.get()
                decoded_msg = self.Response.resolve_message(encoded_msg)
                print(decoded_msg)

    def start_receive(self):
        receive = threading.Thread(target=self.network.receive_msg, args=(self.receive_queue,))
        receive.start()

        process = threading.Thread(target=self.process_receiving)
        process.start()