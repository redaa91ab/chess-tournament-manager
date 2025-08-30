from models import *
from views import *
from rich import print


class PlayersController: 
    def __init__(self, parent):
        self.view = View()
        self.parent = parent

    def players_list(self):
        self.view.show_message(Player.players_list())

    def add_player(self) :
        """ 
        Save the player in players.json by sending the players details to the function save_json of the player model"""

        self.view.show_message("\nEnter the new player details below :")
        id = self.view.get_input("National chess ID : ")
        current_player = Player.return_player_details(id)
        if current_player :
            self.view.show_message("This player already exist")
        elif current_player == None :
            name = self.view.get_input("Name : ")
            surname = self.view.get_input("Surname : ")
            birthdate = self.view.get_input("Birthdate :")
            self.view.show_message("\nPlayer successfully added !")
            player = Player(id, name, surname, birthdate)
            player.save_json()
