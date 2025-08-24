from models import *
from views import *
from rich import print
from .new_tournament import New_Tournament
from .manage_players import ManagePlayers

class Run:
    def __init__(self):
        self.view = View()

    def run(self):
        self.view.show_menu()
        input_live = self.view.get_input("\nChoose an option : ")

        if input_live == "1" or input_live == "1)":
            New_Tournament().new_tournament()
            
        elif input_live == "3" or input_live == "3)" :
            ManagePlayers().manage_players()
        else :
            self.view.show_message("echoue")
