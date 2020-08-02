from server import TCP_Server
import threading
import multiprocessing
import socket
import time



if __name__ == '__main__':
    print("start server")
    host = socket.gethostname()
    port = 23333
    receive_queue = multiprocessing.Queue()
    send_queue = multiprocessing.Queue()
    player_queue = multiprocessing.Queue()
    tcp_server = TCP_Server(host, port, receive_queue, send_queue, player_queue)
    print("!!")
    tcp_server.start()


    while (True):
        time.sleep(1)
        send_queue.put("good".encode("ascii"))