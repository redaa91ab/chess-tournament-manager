from models import *
from views import *
from rich import print



class New_Tournament: 
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
                self.view.show_message("We need more information to add your player ")
                name = self.view.get_input("Name : ")
                surname = self.view.get_input("Surname : ")
                birthdate = self.view.get_input("Birthdate : ")
                player = Player(id, name, surname, birthdate)
                player.save_json()
                add_player = tournament.add_players_fromID(id)
                self.view.show_message(f"{add_player[1].surname} {add_player[1].name} ({add_player[1].id}) was successfully added !\n")

            else :
                self.view.show_message(f"{add_player[1].surname} {add_player[1].name} ({add_player[1].id}) was successfully added !\n")
        
        
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
