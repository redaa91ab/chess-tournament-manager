from models import *
from views import *
from rich import print
from .players_controller import PlayersController
from .tournaments_controller import TournamentsController

class AppController:
    """
    1) Affiche le MainMenu dans view
    2) Demande à l'utilisateur de choisir un sous menu(script) à executer
    3) Execute le script du sous menu choisi
    """

    def __init__(self):
        self.view = View()

    def run(self):
        self.view.main_menu()
        input_live = self.view.get_input("\nChoose an option : ")

        if input_live == "1" or input_live == "1)":
            self.manage_tournaments()    
        elif input_live == "2" or input_live == "2)" :
            self.manage_players()
        elif input_live == "3" or input_live == "3)" :
            pass
        elif input_live == "4" or input_live == "4)" :
            return None
        else :
            self.view.show_message("Erreur veuilez réessayer")
            self.run()

    def manage_tournaments(self):
        self.view.manage_tournaments_menu()
        input_live = self.view.get_input("\nChoose an option : ")
        while input_live == "1" or input_live == "1)": 
            TournamentsController(self).create()
        while input_live == "2" or input_live == "2)":
            TournamentsController(self).add_player_tournament()
        while input_live == "3" or input_live == "3)":
            pass
        while input_live == "4" or input_live == "4)":   
            self.run()

    def manage_players(self):
        self.view.manage_players_menu()
        input_manageplayers = self.view.get_input("\nChoose an option : ")
        while input_manageplayers == "1" or input_manageplayers == "1)" :
            PlayersController(self).players_list()
            self.manage_players()
        while input_manageplayers == "2" or input_manageplayers == "2)" :
            PlayersController(self).add_player()
            self.manage_players()
        while input_manageplayers == "3" or input_manageplayers == "3)" :
            self.run()



    

    

