import asyncio
# import pygame, sys
# from classes.game import Game
import argparse
import socket 
import time
import sys
from chat import Chat
from ipaddress import ip_address, IPv4Address

def main_server(port, value, address_family, ip):
    if address_family == "IPv6":
        address_family = socket.AF_INET6
    else:
        address_family = socket.AF_INET

    client_socket = socket.socket(address_family, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    message = value
    client_socket.send(message.encode())
    
    data = client_socket.recv(1024)
    
    #duerme un seg para asegurar que alcance a levantar la sala de juego
    time.sleep(1)
    game_port = data.decode()
    print(game_port)
    client_socket.close()
    return game_port



async def start_client(port, address_family,ip, character):

    # Determine the IP address family
    socket_family = socket.AF_INET6 if "IPv6" in address_family else socket.AF_INET
    client = socket.socket(socket_family, socket.SOCK_STREAM)
    client.connect((ip, int(port)))
    client.send((character+'\n').encode()) # Send name to server after connecting

    Chat(character, client)
    
def validIPAddress(IP: str) -> str:
    try:
        return "IPv4" if type(ip_address(IP)) is IPv4Address else "IPv6"
    except ValueError:
        return "Invalid"
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Client Game',
        description='Client for playing the game',
        epilog='write -p/--port to pick a port and -n or -j to create new room or join a room')

    group = parser.add_mutually_exclusive_group(required=False)
    
    group.add_argument('-n', '--new', action='store_true', help='Create a new room')
    group.add_argument('-r', '--random', action='store_true', help='Join an existing random room')
    parser.add_argument('-i', '--ip_address', help='Specify the ip of the server to connect')
    parser.add_argument('-p', '--port', type=int, help='Port number')
    parser.add_argument('-c', '--character', help='Character Name')

    args = parser.parse_args()
    if args.ip_address is not None:
        address_family = validIPAddress(args.ip_address)
        if(address_family == 'Invalid'):
            parser.error('Ip not valid')
        ip=args.ip_address
    else:
        parser.error('Ip not valid')
    
    if args.character is None:
        parser.error('Character name is not optional')

        
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
            game_port = main_server(port, value, address_family, ip)
    else: 
        game_port = args.port
    

        
    print(game_port)
    if int(game_port) != 0:
        print(f"Port number: {game_port}")
        print("Connecting to game room")
        print(game_port)
        asyncio.run(start_client(game_port, address_family, ip, args.character))
    else:
        print("Error, that port was not found")


