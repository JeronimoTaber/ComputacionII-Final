from classes.gameRoom import GameRoom
class GameRoomManager:
    def __init__(self):
        self.game_rooms = []

    def create_game_room(self, max_players):
        game_room = GameRoom(max_players)
        self.game_rooms.append(game_room)
        return game_room.uuid

    def add_player_to_game_room(self, game_room_uuid, player):
        for game_room in self.game_rooms:
            if game_room.uuid == game_room_uuid:
                if game_room.add_player(player):
                    return True
                else:
                    return False
        return False
    def remove_player_from_game_room(self, game_room_uuid, player):
        for game_room in self.game_rooms:
            if game_room.uuid == game_room_uuid:
                game_room.remove_player(player)
                if(game_room.get_players() == []):
                    self.game_rooms.remove(game_room)
                return True
        return False
    
    def get_available_game_room(self):
        for game_room in self.game_rooms:
            if len(game_room.players) < game_room.max_players:
                return game_room.uuid
        return None
    
    def get_game_room(self, game_room_uuid):
        for game_room in self.game_rooms:
            if game_room.uuid == game_room_uuid:
                return game_room
        return None
    
    def get_all_rooms(self):
        return self.game_rooms
