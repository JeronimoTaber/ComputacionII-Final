import asyncio
import multiprocessing
import socket
import logging
from classes.gameRoomManager import GameRoomManager
from classes.mainServer import Server
from classes.player import Player

MAX_PLAYERS_PER_ROOM = 4


async def handle_client(reader, writer, game_room_uuid, game_room_manager):
    print(f"New client connected: {writer.get_extra_info('peername')} to room: {game_room_uuid}")

    name = await reader.readline()

    player = Player(name.decode().strip(), writer.get_extra_info('peername'))

    game_room_manager.add_player_to_game_room(game_room_uuid, player)
    game_room = game_room_manager.get_game_room(game_room_uuid)
    print(game_room)
    writer.write(f"{game_room}\n".encode())
    await writer.drain()

    # Game Started
    while True:
        data = await reader.readline()
        if not data or data.decode().strip() == "quit":
            break
        match data.decode().strip():
            case "quit":
                print('Quitting')
                break

            case "room":
                print("creating new room")

        print(f"Received from {writer.get_extra_info('peername')}: {data.decode().strip()}")

    game_room_manager.remove_player_from_game_room(game_room_uuid, player)
    print(f"Client {writer.get_extra_info('peername')} disconnected")
    game_rooms = game_room_manager.get_all_rooms()
    for game_room in game_rooms:
        print(game_room)
    writer.close()
    await writer.wait_closed()


async def start_server(game_room_uuid, port, game_room_manager):
    server = await asyncio.start_server(lambda r, w: handle_client(r, w, game_room_uuid, game_room_manager), "127.0.0.1", port)
    print(f"Server listening on {server.sockets[0].getsockname()}")
    print(f"Room UUILD {game_room_uuid}")

    async with server:
        await server.serve_forever()


def get_random_unused_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))
        return s.getsockname()[1]


def handle(connection, address, game_room_manager):
    try:
        game_room_uuid = game_room_manager.create_game_room(MAX_PLAYERS_PER_ROOM)
        game_rooms = game_room_manager.get_all_rooms()
        print("/////////////////////\n")
        for game_room in game_rooms:
            print(game_room)
            print("\n")

        print("/////////////////////\n")
            
        port = str(get_random_unused_port())
        connection.sendall(port.encode())
        asyncio.run(start_server(game_room_uuid, port, game_room_manager))
    finally:
        connection.close()

from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager

if __name__ == "__main__":
    server = Server("127.0.0.1", 9000)
    print('start')
    try:
        BaseManager.register('GameRoomManager', GameRoomManager)
        manager = BaseManager()
        manager.start()
        inst = manager.GameRoomManager()
        server.start(handle,inst)
    except Exception as e: # work on python 3.x
        logger = logging.getLogger("server")
        logger.error('Failed to upload to ftp: '+ str(e))
        for process in multiprocessing.active_children():
            process.terminate()
            process.join()
