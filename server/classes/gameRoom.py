import uuid 

class GameRoom:
    def __init__(self, max_players):
        self.uuid = uuid.uuid4()
        self.max_players = max_players
        self.players = []

    def add_player(self, player):
        if len(self.players) < self.max_players:
            self.players.append(player)
            return True
        else:
            return False
        
    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)
            return True
        else:
            return False
        
    def get_players(self):
        return self.players
        
    def __str__(self):
        player_strs = [str(player) for player in self.players]
        return f'GameRoom(uuid={self.uuid}, players=[{", ".join(player_strs)}])'
 

