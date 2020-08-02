from client import Player
import socket


if __name__ == "__main__":
    host = socket.gethostname()
    TCP_port = 23333
    UDP_port = 23334

    player = Player("Tom", host, TCP_port, UDP_port, "TCP")
    player.start_send()
    player.start_receive()
