from models import *
from views import *
from rich import print


class ManagePlayers: 
    def __init__(self, parent):
        self.view = View()
        self.manage_players_menu = ManagePlayersMenu()
        self.parent = parent

    def manage_players(self):
        self.manage_players_menu.show()
        input_manageplayers = self.view.get_input("\nChoose an option : ")
        while input_manageplayers == "1" or input_manageplayers == "1)" :
            players = AllPlayers()
            self.view.show_message(players.players_list())
            self.manage_players()

        while input_manageplayers == "2" or input_manageplayers == "2)" :
            self.view.show_message("\nEnter the new player details below :")
            id = self.view.get_input("National chess ID : ")
            current_player = AllPlayers().return_player_details(id)
            if current_player :
                self.view.show_message("This player already exist")

            elif current_player == None :
                name = self.view.get_input("Name : ")
                surname = self.view.get_input("Surname : ")
                birthdate = self.view.get_input("Birthdate :")
                self.view.show_message("\nPlayer successfully added !")
                player = Player(id, name, surname, birthdate)
                player.save_json()
                self.manage_players()
    
        while input_manageplayers == "3" or input_manageplayers == "3)" :
            self.parent.run()
  

"""

            input_live = self.view.get_input("\nChoose an option : ")
            
            while input_live == "1" or input_live == "1)":
                self.view.show_message("\n[bold green]New tournament[/bold green]\n")
                id = self.view.get_input("Add a player (National Chess ID) : ")
                add_player = tournament.add_players_fromID(id) #create the player instance  and save it in tournament
       
                if add_player == None :
                    self.view.show_message("\nThis player doesn't exist :\n1) Try again \n2) Create a new player \n")
                    option = self.view.get_input("Choose an option : ")
                    if option == "1" or option == "1)" :
                        pass
                    
                    elif option == "2" or option == "2)" :
                        name = self.view.get_input("Name : ")
                        surname = self.view.get_input("Surname : ")
                        birthdate = self.view.get_input("Birthdate : ")
                        player = Player(id, name, surname, birthdate)
                        player.save_json()
                        add_player = tournament.add_players_fromID(id)
                        number_players += 1
                        self.view.show_message(f"\n{add_player[1].name} {add_player[1].surname} ({add_player[1].id}) was successfully added !")
                        input_live = "0"                

                else :
                    number_players += 1
                    self.view.show_message(f"\n{add_player[1].surname} {add_player[1].name} ({add_player[1].id}) was successfully added !")
                    input_live = "0"

"""