import asyncio
import pygame, sys

async def send_message(reader, writer):
    playerName = input("select player name: ")
    writer.write(f"{playerName}\n".encode())
    await writer.drain()
    response_game_starts = await reader.readline()
    print(response_game_starts.decode().strip())
    
    #Game Started
    while True:
        message = input("Enter a message to send (type 'quit' to exit): ")
        if not message:
            continue
        writer.write(f"{message}\n".encode())
        await writer.drain()
        if message == "quit":
            break

    writer.close()
    await writer.wait_closed()

async def start_client():
    reader, writer = await asyncio.open_connection("127.0.0.1", 65432)
    print(f"Connected to server: {writer.get_extra_info('peername')}")

    await send_message(reader, writer)

asyncio.run(start_client())