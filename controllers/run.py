from models import *
from views import *
from rich import print
from .new_tournament import NewTournament
from .manage_players import ManagePlayers
from .start_tournament import StartTournament

class Run:
    def __init__(self):
        self.view = View()
        self.MainMenu = MainMenu()
        self.ManagePlayers = ManagePlayers(self)
    def run(self):
        self.MainMenu.show()
        input_live = self.view.get_input("\nChoose an option : ")

        if input_live == "1" or input_live == "1)":
            self.run_start()
            
        elif input_live == "2" or input_live == "2)" :
            self.run_manage_players()

        elif input_live == "3" or input_live == "3)" :
            pass

        elif input_live == "4" or input_live == "4)" :
            return None

        else :
            self.view.show_message("Erreur veuilez réessayer")
            self.run()

    def run_start(self):
        StartTournament(self).start()

    def run_new_tournament(self):
        NewTournament(self).new_tournament()

    def run_manage_players(self):
        ManagePlayers(self).manage_players()



    

    

