import socket
import msvcrt
import threading
from queue import Queue
from utils import Request_Message
from utils import Response_Message
import multiprocessing


class Player:
    def __init__(self, socket, player_IP, player_port):
        self.has_socket = True
        self.socket = socket
        self.player_IP = player_IP
        self.player_port = player_port


class TCP_Server(multiprocessing.Process):
    def __init__(self, server_IP, server_TCP_port, receive_queue, send_queue, player_queue):
        multiprocessing.Process.__init__(self)
        self.valid = True
        self.server_IP = server_IP
        self.server_TCP_port = server_TCP_port
        self.receive_queue = receive_queue
        self.send_queue = send_queue
        self.player_queue = player_queue
        print("init")
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = new_socket

    def setup(self):
        self.socket.bind((self.server_IP, self.server_TCP_port))
        self.socket.listen(5)

    def receive_msg(self, client_socket, receive_queue):
        while (self.valid):
            encoded_msg = client_socket.recv(1024)
            print(encoded_msg.decode())
            receive_queue.put(encoded_msg)

    def listen(self, receive_queue, player_queue):
        while (self.valid):
            client_socket, client_add = self.socket.accept()
            print("new client")
            new_player = Player(client_socket, client_add[0], client_add[1])
            player_queue.put(new_player)
            new_client = threading.Thread(target=self.receive_msg, args=(client_socket, receive_queue))
            new_client.start()

    def send_msg(self, send_queue, client_socket):
        while (self.valid):
            if not send_queue.empty():
                encoded_msg = send_queue.get()
                client_socket.send(encoded_msg)

    def run(self):
        self.setup()

        start_send = threading.Thread(target=self.listen, args=(self.receive_queue, self.player_queue))
        start_send.start()

        new_player = self.player_queue.get()
        start_send = threading.Thread(target=self.send_msg, args=(self.send_queue, new_player.socket,))
        start_send.start()


class Map:
    def __init__(self):
        pass