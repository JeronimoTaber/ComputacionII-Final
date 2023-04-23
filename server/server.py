import asyncio
import multiprocessing
import socket
import logging
from classes.gameRoomManager import GameRoomManager
from mainServer import Server
from classes.player import Player
from multiprocessing import Manager
from multiprocessing.managers import BaseManager
from periodic import Periodic

if __name__ == "__main__":
    
    server = Server("127.0.0.1", 9000)
    try:
        BaseManager.register('GameRoomManager', GameRoomManager)
        manager = BaseManager()
        manager.start()
        game_room_manager_instance = manager.GameRoomManager()
        lock_instance = Manager().Lock()
        server.start(game_room_manager_instance, lock_instance)
        
    except Exception as e:
        logger = logging.getLogger("server")
        logger.error('Failed to upload to ftp: '+ str(e))
        for process in multiprocessing.active_children():
            process.terminate()
            process.join()
