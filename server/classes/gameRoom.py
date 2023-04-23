import uuid 
from colorama import Fore, Back, Style
import datetime
import dill as pickle
class GameRoom:
    def __init__(self, max_players, port):
        self.creation_time = datetime.datetime.now()
        self.uuid = uuid.uuid4()
        self.max_players = max_players
        self.players = set()  # Change to set
        self.port = port

    def add_player(self, player):
        if len(self.players) < self.max_players:
            self.players.add(player)  # Use add() instead of append()
            return True
        else:
            return False

    def remove_player(self, player_to_delete):
        for player in self.players:
            if player.name == player_to_delete.name and player.player_uuid == player_to_delete.player_uuid:                
                self.players.remove(player)
                return True

        else:
            return False
        
    def get_players(self):
        return self.players
    
    def get_port(self):
        return self.port
    
    def set_port(self, port):
        self.port = port
        return True 

    def __str__(self):
        player_strs = [str(player) for player in self.players]
        return f'GameRoom(uuid={self.uuid}, players=[{", ".join(player_strs)}])'

