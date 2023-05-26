import multiprocessing
import socket
import asyncio
from handleClient import startServer
from logger import setup_logging
MAX_PLAYERS_PER_ROOM = 4
from periodic import Periodic
def get_random_unused_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))
        return s.getsockname()[1]
    
def handle(connection, address, game_room_manager, lock):
    try:

        game_rooms = game_room_manager.get_all_rooms()
        print("/////////////////////\n")
        for game_room in game_rooms:
            print(game_room)
            print("\n")

        print("/////////////////////\n")
            

        with lock:
            port = str(get_random_unused_port())
            connection.sendall(port.encode())
            try:
                game_room_uuid = game_room_manager.create_game_room(MAX_PLAYERS_PER_ROOM, port)
            except Exception as e:
                print(e)
                raise Exception(e) 
        asyncio.run(startServer(game_room_uuid, port, game_room_manager, lock)) #Check si se puede sacar asyncio y solo llamr a la funcion?
    except Exception as e:
        print(e)
        raise Exception(e) 

    finally:
        connection.close()

    
class Server(object):
    def __init__(self, hostname, port):
        self.logger = setup_logging("server")
        self.hostname = hostname
        self.port = port
 
   

    def start(self, game_room_manager, lock):
        print("listening")
        self.logger.debug("listening")
        # Crea socket que permite ipv4 y ipv6
        try:
            # Try creating an IPv6 socket
            self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.hostname, self.port))
        except OSError as e:
            if "Address family not supported by protocol" in str(e):
                # IPv6 not supported, fallback to IPv4
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.socket.bind((self.hostname, self.port))
            else:
                # Unexpected error, raise it
                print(e)
                raise
        self.socket.listen(5)
        while True:
            try:
                conn, address = self.socket.accept()
                game_room_manager.remove_unused_game_rooms()
                self.logger.debug("Got connection")
                print("Got connection")

                action = conn.recv(1024)  
                decoded_message = action.decode('utf-8')
                if decoded_message == "new":
                    self.logger.debug("Creating new game")
                    process = multiprocessing.Process(target=handle, args=(conn, address, game_room_manager, lock))
                    process.daemon = True
                    process.start()
                    self.logger.debug("Started process %r", process)
                elif decoded_message == "random":
                    game_room = game_room_manager.get_random_game_room();
                    if(game_room is None):
                        print("No available game room")
                        message = "0"
                        conn.send(message.encode())
                    else:
                        print("Available game room")
                        print(game_room)
                        message = str(game_room.port)
                        conn.send(message.encode())
                    conn.close()
                else:
                    # Handle unknown options
                    print(f"Received unknown option from client: {decoded_message}")
            except Exception as e:
                print (e)
