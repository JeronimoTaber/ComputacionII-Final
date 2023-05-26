from classes.player import Player
import asyncio
import dill as pickle
import openai
from tasks import add, chat_complete_task
import socket
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
            case "exit":
                print('Quitting')
                message = {
                "role": "user", "content": f"[{name.decode().strip()}]: [I'm leaving the game]"}
                for remote_writer in clients_writers:
                    if(remote_writer.writer != localStore.writer):
                        clients_writers.add()
                        remote_writer.writer.write(('\n'+name.decode().strip()+' Message: \n'+data.decode().strip()).encode())
                        
                await remote_writer.writer.drain()

                break

        print(
            f"Received from {writer.get_extra_info('peername')}: {data.decode().strip()}")
        message = {
            "role": "user", "content": f"[{name.decode().strip()}]: [{data.decode().strip()}]"}
        for remote_writer in clients_writers:
            if(remote_writer.writer != localStore.writer):
                remote_writer.writer.write(('\n'+name.decode().strip()+': \n'+data.decode().strip()).encode())
                
        await remote_writer.writer.drain()

        with lock:
            messages = game_room_manager.get_messages(game_room_uuid)

            messages.append(message)
            variable = "ERROR"
            try:
                response = chat_complete_task.delay(messages)
                variable = response.get()
                game_room_manager.add_message_to_game_room(game_room_uuid, message)
                response_message = {"role": "assistant", "content": f"{variable}"}
                game_room_manager.add_message_to_game_room(
                    game_room_uuid, response_message)
            except Exception as e:  
                print(e)     
                variable = "Error"

        for remote_writer in clients_writers:
            remote_writer.writer.write(('DM: \n'+variable).encode())
            await remote_writer.writer.drain()

    with lock:
        game_room_manager.remove_player_from_game_room(game_room_uuid, player)
    print(f"Client {writer.get_extra_info('peername')} disconnected")
    writer.close()
    await writer.wait_closed()


async def startServer(game_room_uuid, port, game_room_manager, lock):
    clients_writers = set()
    #UTILIZA LA DIRECCION IPV6 WILDCARD QUE  ESPECIFICANDO family=socket.AF_UNSPEC ACEPTA CONECCIONES DE IPV4 e IPV6\

    try:
        serverIPV4 = await asyncio.start_server(lambda r, w: handleClient(r, w, game_room_uuid, game_room_manager, lock, clients_writers), "localhost", port) 

        serverIPV6 = await asyncio.start_server(
            lambda r, w: handleClient(r, w, game_room_uuid, game_room_manager, lock, clients_writers),
            "::",
            port,
            family=socket.AF_UNSPEC
        )    
    except Exception as e:
        print (e)
    # server = await asyncio.start_server(lambda r, w: handleClient(r, w, game_room_uuid, game_room_manager, lock, clients_writers), "127.0.0.1", port) 



    async with serverIPV4 and serverIPV6:
        await serverIPV4.wait_closed() and await serverIPV6.wait_closed() 
