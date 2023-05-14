import asyncio
# import pygame, sys
# from classes.game import Game
import argparse
import socket 
import time
def main_server(port, value):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    message = value
    client_socket.send(message.encode())
    
    data = client_socket.recv(1024)
    
    #duerme un seg para asegurar que alcance a levantar la sala de juego
    time.sleep(1)
    game_port = data.decode()
    print(game_port)
    client_socket.close()
    return game_port

async def read_messages(reader):
    while True:
        message = await reader.read(65535)        
        print('\n Response: \n')
        print(message.decode().strip())
        print('\n End Response \n ---------- \n')

async def game_server(reader, writer):
    print('Connected to game server')
    name = input('Name: ')
    writer.write(f"{name}\n".encode())
    await writer.drain()

    asyncio.create_task(read_messages(reader))
    while True:
        message = await asyncio.to_thread(input, f"{name}: ")
        writer.write(f"{message}\n".encode())
        await writer.drain()

    
    writer.close()
    await writer.wait_closed()

async def start_client(port):
    
    reader, writer = await asyncio.open_connection("127.0.0.1", port)
    await game_server(reader,writer)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Client Game',
        description='Client for playing the game',
        epilog='write -p/--port to pick a port and -n or -j to create new room or join a room')

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-n', '--new', action='store_true', help='Create a new room')
    group.add_argument('-r', '--random', action='store_true', help='Join an existing random room')

    parser.add_argument('-p', '--port', type=int, help='Port number')

    args = parser.parse_args()

    if args.port is None or args.port == 9000:
        port = 9000
        if not args.new and not args.random:
            parser.error('One of -n or -r is required with port 9000 or None')
        elif args.new and args.random:
            parser.error('Only one of -n or -r can be specified')
        else:
            print("Connecting to main server")
            print(args.new)
            value = "new" if args.new is not False else "random"
            print (value)
            game_port = main_server(port, value)
    else: 
        game_port = args.port
    print(game_port)
    if int(game_port) != 0:
        print(f"Port number: {game_port}")
        print("Connecting to game room")
        print(game_port)
        asyncio.run(start_client(game_port))
    else:
        print("Error, no se encuentra un puerto disponible")


