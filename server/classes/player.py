class Player:
    def __init__(self, name, player_uuid):
        self.name = name
        self.player_uuid = player_uuid
        self.writer = None
        
    def __str__(self) -> str:
        return f'name={self.name}, player_uuid=({self.player_uuid})), {self.writer}'
    
    def set_name (self, name):
        self.name = name
        return True
    
    def set_writer (self, writer):
        self.writer = writer
        return True