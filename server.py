import socket
import msvcrt
import threading
from queue import Queue
from utils import Request_Message
from utils import Response_Message
import multiprocessing
import time


class Player:
    def __init__(self, socket, player_IP, player_port):
        self.has_socket = True
        self.socket = socket
        self.player_IP = player_IP
        self.player_port = player_port
        self.msg = None

    def update_msg(self, msg):
        self.msg = msg

class TCP_Server():
    def __init__(self, server_IP, server_TCP_port):
        self.valid = True
        self.server_IP = server_IP
        self.server_TCP_port = server_TCP_port

    def setup(self):
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = new_socket
        self.socket.bind((self.server_IP, self.server_TCP_port))
        self.socket.listen(5)

    def receive_msg(self, player, receive_queue):
        while (self.valid):
            try:
                encoded_msg = player.socket.recv(1024)
                print(encoded_msg.decode())
                player.update_msg(encoded_msg)
                receive_queue.put(player)
            except ConnectionResetError:
                print("client dropped - receiving closed")
                time.sleep(1)
                break

    def listen(self, receive_queue, player_queue):
        while (self.valid):
            client_socket, client_add = self.socket.accept()
            print("new client")
            new_player = Player(client_socket, client_add[0], client_add[1])
            player_queue.put(new_player)
            new_client = threading.Thread(target=self.receive_msg, args=(new_player, receive_queue))
            new_client.start()

    def send_msg(self, send_queue):
        while (self.valid):
            if not send_queue.empty():
                player = send_queue.get()
                encoded_msg = player.msg
                try:
                    player.socket.send(encoded_msg)
                except ConnectionResetError:
                    print("client dropped - sending ceased")

    def start(self, receive_queue, send_queue, player_queue):
        self.setup()

        start_send = threading.Thread(target=self.listen, args=(receive_queue, player_queue))
        start_send.start()

        start_send = threading.Thread(target=self.send_msg, args=(send_queue,))
        start_send.start()


class Map:
    def __init__(self):
        pass