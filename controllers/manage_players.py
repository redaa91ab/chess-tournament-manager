from models import *
from views import *
from rich import print


class ManagePlayers: 
    def __init__(self):
        self.view = View()
        

    def manage_players(self):
        from .run import Run
        self.view.show_message("\n[bold green]Manage Players :[/bold green]\n")
        self.view.show_message("1) See all players")
        self.view.show_message("2) Add players")
        self.view.show_message("[red]3) Back [/red]")
        input_manageplayers = self.view.get_input("\nChoose an option : ")

        if input_manageplayers == "1" or input_manageplayers == "1)" :
            players = Player()
            self.view.show_message(players.show_players_json())
            self.manage_players()

        elif input_manageplayers == "2" or input_manageplayers == "2)" :
            self.view.show_message("\nEnter the new player details below :")
            id = self.view.get_input("National chess ID : ")
            name = self.view.get_input("Name : ")
            surname = self.view.get_input("Surname : ")
            birthdate = self.view.get_input("Birthdate : ")
            player = Player(id, name, surname, birthdate )
            player.save_json()
            self.manage_players
        elif input_manageplayers == "3" or input_manageplayers == "3)" :
            Run().run()

