from classes.player import Player
import asyncio


async def handleClient(reader, writer, game_room_uuid, game_room_manager, lock):
    print(f"New client connected: {writer.get_extra_info('peername')} to room: {game_room_uuid}")

    name = await reader.readline()

    player = Player(name.decode().strip(), writer.get_extra_info('peername'))
    with lock:
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
    with lock:
        game_room_manager.remove_player_from_game_room(game_room_uuid, player)
    print(f"Client {writer.get_extra_info('peername')} disconnected")
    game_rooms = game_room_manager.get_all_rooms()
    for game_room in game_rooms:
        print(game_room)
    writer.close()
    await writer.wait_closed()

async def startServer(game_room_uuid, port, game_room_manager, lock):
    server = await asyncio.start_server(lambda r, w: handleClient(r, w, game_room_uuid, game_room_manager, lock), "127.0.0.1", port)
    print(f"Server listening on {server.sockets[0].getsockname()}")
    print(f"Room UUILD {game_room_uuid}")

    async with server:
        await server.serve_forever()