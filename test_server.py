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

    tcp_server = TCP_Server(host, port)
    start_TCP = multiprocessing.Process(target=tcp_server.start, args=(receive_queue, send_queue, player_queue))
    start_TCP.start()
    count = 0

    player = player_queue.get()
    while (True):
        count += 1
        time.sleep(1)
        player.update_msg("good".encode("ascii"))
        send_queue.put(player)
        if (count == 20):
            print("someone")
            player = player_queue.get()