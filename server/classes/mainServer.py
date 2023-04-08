import multiprocessing
import socket
import asyncio
from handle_client import startServer

MAX_PLAYERS_PER_ROOM = 4

def get_random_unused_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))
        return s.getsockname()[1]
    
def handle(connection, address, game_room_manager, lock):
    try:
        with lock:
            game_room_uuid = game_room_manager.create_game_room(MAX_PLAYERS_PER_ROOM)
        game_rooms = game_room_manager.get_all_rooms()
        print("/////////////////////\n")
        for game_room in game_rooms:
            print(game_room)
            print("\n")

        print("/////////////////////\n")
            
        port = str(get_random_unused_port())
        connection.sendall(port.encode())
        asyncio.run(startServer(game_room_uuid, port, game_room_manager, lock))
    finally:
        connection.close()
        
class Server(object):
    def __init__(self, hostname, port):
        import logging
        self.logger = logging.getLogger("server")
        self.hostname = hostname
        self.port = port

    def start(self, game_room_manager, lock):
        
        self.logger.debug("listening")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(5)

        while True:
            conn, address = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=handle, args=(conn, address, game_room_manager, lock))
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)
