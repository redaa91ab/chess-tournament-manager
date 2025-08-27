from models import *
from views import *
from rich import print



class NewTournament: 
    def __init__(self, parent):
        self.view = View()
        self.new_tournament_menu = NewTournamentMenu()
        self.parent = parent

    def new_tournament(self):

        #tournament_informations
        self.view.show_message("\n[bold green]New tournament[/bold green]\n")
        self.view.show_message("Enter the new tournament details below : ")
        tournament_name = self.view.get_input("Tournament name : ")
        place = self.view.get_input("Place : ")
        start_date = self.view.get_input("Start date : ")
        end_date = self.view.get_input("End date : ")
        number_rounds = self.view.get_input("Number of rounds : ")
        tournament = Tournament(tournament_name, place, start_date, end_date, number_rounds)
        tournament.save_json()
        
        number_players = 0      
        
        #Main Menu
        while self.new_tournament:

            self.new_tournament_menu.show()
            input_live = self.view.get_input("\nChoose an option : ")
            
            while input_live == "1" or input_live == "1)":
                self.view.show_message("\n[bold green]New tournament[/bold green]\n")
                id = self.view.get_input("Add a player (National Chess ID) : ")
                add_player = AllPlayers().return_player_details(id) #create the player instance  and save it in tournament
            
                if add_player == None :
                    self.view.show_message("\nThis player doesn't exist :\n1) Try again \n2) Create a new player \n")
                    option = self.view.get_input("Choose an option : ")
                    if option == "1" or option == "1)" :
                        pass
                    
                    elif option == "2" or option == "2)" :
                        name = self.view.get_input("Name : ")
                        surname = self.view.get_input("Surname : ")
                        birthdate = self.view.get_input("Birthdate : ")
                        Player(id, name, surname, birthdate).save_json()
                        tournament.players.append(id)
                        tournament.save_json()
                        self.view.show_message(f"\n{name} {surname} ({id}) was successfully added !")
                        number_players += 1
                        input_live = "0"         

                else :
                    tournament.players.append(id)
                    tournament.save_json()
                    self.view.show_message(f"\n{add_player[1]} {add_player[2]} ({add_player[0]}) was successfully added !")
                    number_players += 1
                    input_live = "0"

            while input_live == "2" or input_live == "2)" :
                pass

            while input_live == "3" or input_live == "3)" :
                self.parent.run()


