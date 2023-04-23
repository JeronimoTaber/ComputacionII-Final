from classes.gameRoom import GameRoom
import random
import datetime


class GameRoomManager:
    def __init__(self):
        self.game_rooms = set()

    def create_game_room(self, max_players, port):
        game_room = GameRoom(max_players, port)
        self.game_rooms.add(game_room)
        return game_room.uuid

    def add_player_to_game_room(self, game_room_uuid, player):
        game_room = self.get_game_room(game_room_uuid)
        if game_room:
            if game_room.add_player(player):
                return True
            else:
                return False
        return False

    def get_players_in_game_room(self, game_room_uuid):
        game_room = self.get_game_room(game_room_uuid)
        if game_room:
            return game_room.get_players()
        else:
            return None
        
    def get_other_players_in_game_room(game_room_manager, game_room_uuid, player_uuid):
        players = game_room_manager.get_players_in_game_room(game_room_uuid)
        other_players = []
        for player in players:
            if player.player_uuid != player_uuid:
                other_players.append(player)
        return other_players

    def add_port_to_game_room(self, game_room_uuid, port):
        game_room = self.get_game_room(game_room_uuid)
        if game_room:
            if game_room.add_port(port):
                return True
            else:
                return False
        return False

    def remove_player_from_game_room(self, game_room_uuid, player_to_delete):
        game_room = self.get_game_room(game_room_uuid)
        if game_room:
            game_room.remove_player(player_to_delete)
            if (game_room.get_players() == set()):
                self.game_rooms.remove(game_room)
            return True
        return False

    def remove_game_room(self, game_room_uuid):
        game_room = self.get_game_room(game_room_uuid)
        if game_room:
            self.game_rooms.remove(game_room)
            return True
        return False

    def remove_unused_game_rooms(self):
        current_time = datetime.datetime.now()
        for game_room in self.game_rooms:
            elapsed_time = current_time - game_room.creation_time
            if game_room.get_players() == set() and elapsed_time >= datetime.timedelta(seconds=10):
                self.game_rooms.remove(game_room)

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

    def get_random_game_room(self):
        available_rooms = []
        for game_room in self.game_rooms:
            if len(game_room.players) < game_room.max_players:
                available_rooms.append(game_room)

        if len(available_rooms) > 0:
            return random.choice(available_rooms)
        else:
            return None