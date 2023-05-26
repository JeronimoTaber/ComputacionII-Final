import uuid
from colorama import Fore, Back, Style
import datetime
import dill as pickle
from classes.chatGpt import sendMessage
import concurrent.futures
import os
import openai
import asyncio


class GameRoom:
    # Load your API key
    # from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    def __init__(self, max_players, port):
        self.creation_time = datetime.datetime.now()
        self.uuid = uuid.uuid4()
        self.max_players = max_players
        self.players = set()  # Change to set
        self.port = port
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'chatSetting.txt')
        text = self.extract_text_from_file(file_path)
        if text is None:
            raise Exception("Initial text not found") 
        self.messages = [{"role": "system",
                          "content":text
                          },
                         {"role": "assistant",
                             "content": "Hello"}]
        
    def extract_text_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()
            return text
        except IOError:
            print(f"Error: Could not read the file '{file_path}'")
            return None

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

    def add_message(self, content):
        print(content)
        self.messages.append(content)
        # self.messages.append({"role": "assistant", "content": response})
        return True

    def __str__(self):
        player_strs = [str(player) for player in self.players]
        return f'GameRoom(uuid={self.uuid}, players=[{", ".join(player_strs)}])'
