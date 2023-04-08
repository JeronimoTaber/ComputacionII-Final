import asyncio
import os
import multiprocessing
from classes.gameRoom import GameRoom
import uuid 
from classes.gameRoomManager import GameRoomManager
from classes.player import Player


game_room_manager = GameRoomManager()
MAX_PLAYERS_PER_ROOM = 4

async def handle_client(reader, writer):
    print(f"New client connected: {writer.get_extra_info('peername')}")
    name = await reader.readline()

    player = Player(name.decode().strip(), writer.get_extra_info('peername'))
    
    
    game_room_uuid = game_room_manager.get_available_game_room();
    if (game_room_uuid == None):
        game_room_uuid = game_room_manager.create_game_room(MAX_PLAYERS_PER_ROOM)
    game_room_manager.add_player_to_game_room(game_room_uuid, player)
    game_room = game_room_manager.get_game_room(game_room_uuid)
    
    print(game_room)
    writer.write(f"{game_room}\n".encode())
    await writer.drain()
    
    
    #Game Started
    while True:
        data = await reader.readline()
        if not data or data.decode().strip() == "quit":
            break
        match data.decode().strip():
            case "quit":
                print('Quiting')
                break

            case "room":
                print ("creating new room")
                
        print(f"Received from {writer.get_extra_info('peername')}: {data.decode().strip()}")
    game_room_manager.remove_player_from_game_room(game_room_uuid, player)
    print(f"Client {writer.get_extra_info('peername')} disconnected")
    writer.close()
    await writer.wait_closed()

async def start_server():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 65432)
    print(f"Server listening on {server.sockets[0].getsockname()}")

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(start_server())