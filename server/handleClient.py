from classes.player import Player
import asyncio
import dill as pickle
import socket
async def handleClient(reader, writer, game_room_uuid, game_room_manager, lock, clients_writers):
    print(f"New client connected: {writer.get_extra_info('peername')} to room: {game_room_uuid}")
    player = Player("", writer.get_extra_info('peername'))
    name = await reader.readline()
    player.set_name(name)
    
    localStore = Player(name, writer.get_extra_info('peername'))
    localStore.set_writer(writer)
    clients_writers.add(localStore)
    with lock:
        if(name is not None):

            game_room_manager.add_player_to_game_room(game_room_uuid, player)
    game_room = game_room_manager.get_game_room(game_room_uuid)


    # Game Started
    while True:
        data = await reader.readline()
        if not data:
            break
        match data.decode().strip():
            case "quit":
                print('Quitting')
                break

            case "room":
                print("creating new room")

        print(f"Received from {writer.get_extra_info('peername')}: {data.decode().strip()}")
        other_players = game_room_manager.get_other_players_in_game_room(game_room_uuid, player.player_uuid)
        for remote_player in other_players:
            for remote_writer in clients_writers:
                if remote_writer.player_uuid == remote_player.player_uuid:
                    remote_writer.writer.write(data)
                    await remote_writer.writer.drain()
            
    with lock:
        game_room_manager.remove_player_from_game_room(game_room_uuid, player)
    print(f"Client {writer.get_extra_info('peername')} disconnected")
    writer.close()
    await writer.wait_closed()

async def startServer(game_room_uuid, port, game_room_manager, lock):
    clients_writers = set()
    server = await asyncio.start_server(lambda r, w: handleClient(r, w, game_room_uuid, game_room_manager, lock, clients_writers), "127.0.0.1", port)
    print(f"Server listening on {server.sockets[0].getsockname()}")
    print(f"Room UUILD {game_room_uuid}")

    async with server:
        await server.wait_closed()

