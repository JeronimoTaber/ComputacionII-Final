from classes.player import Player
import asyncio
import dill as pickle
import openai
import openai_async
import os


async def handleClient(reader, writer, game_room_uuid, game_room_manager, lock, clients_writers):
    print(
        f"New client connected: {writer.get_extra_info('peername')} to room: {game_room_uuid}")
    player = Player("", writer.get_extra_info('peername'))
    name = await reader.readline()
    player.set_name(name)

    localStore = Player(name, writer.get_extra_info('peername'))
    localStore.set_writer(writer)
    clients_writers.add(localStore)
    with lock:
        if (name is not None):

            game_room_manager.add_player_to_game_room(game_room_uuid, player)
    game_room = game_room_manager.get_game_room(game_room_uuid)
    print(game_room)

    # Game Started
    while True:
        data = await reader.readline()
        print('--------')
        print('\n data: \n')
        print(data)
        print('--------')
        if not data:
            break
        match data.decode().strip():
            case "quit":
                print('Quitting')
                break

            case "room":
                print("creating new room")

        print(
            f"Received from {writer.get_extra_info('peername')}: {data.decode().strip()}")
        message = {
            "role": "user", "content": f"[{name.decode().strip()}]: [{data.decode().strip()}]"}
        with lock:
            messages = game_room_manager.get_messages(game_room_uuid)

            messages.append(message)
            response = "ERROR"
            try:
                completion = await openai_async.chat_complete(
                    os.getenv("OPENAI_API_KEY"),
                    timeout=2,
                    payload={
                        "model": "gpt-3.5-turbo",
                        "messages": messages,
                    },
                )
                response = completion.json()["choices"][0]["message"]["content"].strip()
                game_room_manager.add_message_to_game_room(game_room_uuid, message)
                response_message = {"role": "assistant", "content": f"{response}"}
                game_room_manager.add_message_to_game_room(
                    game_room_uuid, response_message)
            except:       
                response = "Error"
                

        print(clients_writers)
        for remote_writer in clients_writers:
            remote_writer.writer.write(('\n'+name.decode().strip()+' Message: \n'+data.decode().strip(
            )+'\nResponse: \n'+response).encode())
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
