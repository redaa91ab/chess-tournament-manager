from models import *
from view import *
from rich import print

class Controller: 
    def __init__(self):
        self.view = View()


    def new_tournament(self):

        #tournament_informations
        self.view.show_message("\n[bold green]New tournament[/bold green]\n")
        self.view.show_message("Enter the new tournament details below : ")
        tournament_name = self.view.get_input("Tournament name : ")
        place = self.view.get_input("Place : ")
        number_rounds = self.view.get_input("Number of rounds : ")
        tournament = Tournament(tournament_name, place, number_rounds)

        #add first 4 players
        number_players = 0
        self.view.show_message("\n[bold green]New tournament[/bold green]\n")
        while number_players < 4 :
            id = self.view.get_input("Add a player (National Chess ID) :")
            add_player = tournament.add_players_fromID(id) #create the player instance  and save it in tournament
            number_players += 1

            if add_player == None :
                name = self.view.get_input("Name : ")
                surname = self.view.get_input("Surname : ")
                birthdate = self.view.get_input("Birthdate : ")
                player = Player(id, name, surname, birthdate)
                player.save_json()
                tournament.add_players_fromID(id)
        
        
        #Menu
        while self.new_tournament:

            self.view.show_message("\n[bold green]New tournament[/bold green]")
            self.view.show_message("\n1) Add new players")
            self.view.show_message("2) Start the tournament")
            self.view.show_message("3)[red] Back[/red]")
            input_live = self.view.get_input("\nChoose an option : ")
            if input_live == "1" or input_live == "1)":
                self.view.show_message("\n[bold green]New tournament[/bold green]\n")
                for i in range(2) :
                
                    id = self.view.get_input("Add a player (National Chess ID) :")
                    add_player = tournament.add_players_fromID(id)
                    number_players += 1

                    if add_player == None :
                        name = self.view.get_input("Name : ")
                        surname = self.view.get_input("Surname : ")
                        birthdate = self.view.get_input("Birthdate : ")
                        player = Player(id, name, surname, birthdate)
                        player.save_json()
                        tournament.add_players_fromID(id)

        
    def ManagePlayers(self):
        self.view.show_message("\n[bold green]Manage Players :[/bold green]\n")
        self.view.show_message("1) See all players")
        self.view.show_message("2) Add players")
        self.view.show_message("[red]3) Back [/red]")
        input_manageplayers = self.view.get_input("\nChoose an option : ")

        if input_manageplayers == "1" or input_manageplayers == "1)" :
            players = Player()
            players.show_players_json()
            self.ManagePlayers()

        elif input_manageplayers == "2" or input_manageplayers == "2)" :
            self.view.show_message("\nEnter the new player details below :")
            id = self.view.get_input("National chess ID : ")
            name = self.view.get_input("Name : ")
            surname = self.view.get_input("Surname : ")
            birthdate = self.view.get_input("Birthdate : ")
            player = Player(id, name, surname, birthdate )
            player.save_json()
            self.ManagePlayers()
        elif input_manageplayers == "3" or input_manageplayers == "3)" :
            self.run()

    def run(self):
        self.view.show_menu()
        input_live = self.view.get_input("\nChoose an option : ")

        if input_live == "1" or input_live == "1)":
            self.new_tournament()

        elif input_live == "3" or input_live == "3)" :
            self.ManagePlayers()
        else :
            print("echoue")
