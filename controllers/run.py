from models import *
from views import *
from rich import print
from .new_tournament import NewTournament
from .manage_players import ManagePlayers

class Run:
    def __init__(self):
        self.view = View()
        self.MainMenu = MainMenu()
        self.ManagePlayers = ManagePlayers(self)
    def run(self):
        self.MainMenu.show()
        input_live = self.view.get_input("\nChoose an option : ")

        if input_live == "1" or input_live == "1)":
            NewTournament(self).new_tournament()
            
        elif input_live == "3" or input_live == "3)" :
            ManagePlayers(self).manage_players()

        elif input_live == "5" or input_live == "5)" :
            pass

        else :
            self.view.show_message("Erreur veuilez réessayer")
            self.run()
