from model import *
from view import *
from rich import print

class Controller: 
    def __init__(self):
        self.view = View()

    def ManagePlayers(self):
        self.view.show_message("\n[bold green]Manage Players :[/bold green]\n")
        self.view.show_message("1) See all players")
        self.view.show_message("2) Add players")
        self.view.show_message("[red]3) Back [/red]")
        input_manageplayers = self.view.get_input("\nChoose an option : ")

        if input_manageplayers == "1" or input_manageplayers == "1)" :
            json_instance = Json()
            json_instance.show_players()
            self.ManagePlayers()

        elif input_manageplayers == "2" or input_manageplayers == "2)" :
            self.view.show_message("\nEnter the new player details below :")
            surname = self.view.get_input("Name : ")
            name = self.view.get_input("Surname : ")
            birthdate = self.view.get_input("Birthdate : ")
            id = self.view.get_input("id : ")
            player = Player(surname, name, birthdate, id)
            player.save_json()
            self.ManagePlayers()
        elif input_manageplayers == "3" or input_manageplayers == "3)" :
            self.run()

    def run(self):
        self.view.show_menu()
        input_live = self.view.get_input("\nChoose an option : ")
        if input_live == "3" or input_live == "3)" :
            self.ManagePlayers()
        else:
            print("echoue")
