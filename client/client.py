import asyncio
import pygame, sys
from classes.game import Game
import argparse
import socket 
import time
def main_server(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    data = client_socket.recv(1024)
    
    #duerme un seg para asegurar que alcance a levantar la sala de juego
    time.sleep(1)
    message = data.decode()
    game_port = message
    print(game_port)
    client_socket.close()
    return game_port

async def game_server(reader, writer):
    print('Connected to game server')
    name = input('Name: ')
    writer.write(f"{name}\n".encode())
    await writer.drain()
    game = Game()
    game.run(reader, writer)
        
    writer.close()
    await writer.wait_closed()

async def start_client(port):
    
    reader, writer = await asyncio.open_connection("127.0.0.1", port)
    await game_server(reader,writer)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Client Game',
                    description='Client for playing the game',
                    epilog='write -p/--port to pick a port')
    parser.add_argument('-p', '--port', type=int, help='Port number')

    args = parser.parse_args()

    port = args.port
    game_port = port
    if port is None or port == 9000:
        print(f"Port number: {port}")
        print("Connecting to main server")
        game_port = main_server(port)

    print(f"Port number: {game_port}")
    print("Connecting to game room")
    print(game_port)
    asyncio.run(start_client(game_port))

