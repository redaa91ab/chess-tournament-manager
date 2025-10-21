from models import Tournament, Player
from datetime import datetime



class TournamentsController:
    """
    A controller class for managing tournament.
    It provides methods to create a new tournament in tournaments.json and add new players to a tournament
    """

    def __init__(self, view):
        """
        Initialize a TournamentsController instance.

        Args:
            view: An instance of the View class
        """
        self.view = view
        self.round = RoundController(self.view)

    def create(self):
        """
        Collect new tournament details and save it in tournaments.json by using the methods save_json of the model Tournament
        """
        self.view.show_message("\n[bold green]Create tournament[/bold green]\n")
        self.view.show_message("Enter the new tournament details below : ")
        tournament_name = self.view.get_input("Tournament name : ").upper()
        place = self.view.get_input("Place : ")
        start_date = self.view.get_input("Start date (DD/MM/YYYY) : ")
        number_of_rounds = self.view.get_input("Number of rounds : ")

        try:
            if Tournament.get_tournament_details(tournament_name) != None :
                raise ValueError("This tournament name is already taken")
            
            number_of_rounds = int(number_of_rounds)
            datetime.strptime(start_date, "%d/%m/%Y")

        except ValueError as e:
            self.view.show_message(f"Invalid input: {e}")
            return

        tournament = Tournament(tournament_name, place, start_date, number_of_rounds)
        tournament.save_json()

    def add_player_tournament(self, tournament_id = None):
        """
        Add players to a tournament in tournaments.json

        Args:
            tournament_name : The name of the tournament to add players to.
                              If None, prompts the user to enter a tournament name.

        Collect the tournament name if not provided and add player to the tournament in tournaments.json.
        If a player doesn't exist, offers the option to create a new player or try again.
        """

        tournaments = Tournament.get_all_tournaments()
  
        while tournament_id == None :
            self.view.show_tournaments_list(tournaments)
            user_input = self.view.get_input("\nEnter the tournament id : ") 
            if int(user_input) in tournaments :
                tournament_id = int(user_input)
            else :
                self.view.show_message("We didn't find any match, please try again")

        while True :
            tournament_details = tournaments[tournament_id]
            tournament_name = tournament_details["tournament_name"]
            self.view.show_message(f"[bold green]\n{tournament_name}[/bold green]")
            self.view.show_add_players_tournament_menu()
            user_choice = self.view.get_input("\nChoose an option : ")

            if user_choice == "1" or user_choice == "1)":
                self.view.show_message(f"\n[bold green]\n{tournament_name}[/bold green]\n")
                national_chess_id = self.view.get_input("Add a player (National Chess ID) : ")
                player = Player.get_player_details(national_chess_id)
                if player in Player.get_all_players():
                    #Tournament.add_player(tournament_id, national_chess_id)
                    Tournament.update_element(tournament_id, "players", [national_chess_id, 0.0])
                    self.view.show_message(f"\n{player["name"]} {player["surname"]} ({player["national_chess_id"]}) was successfully added !")
                elif player not in Player.get_all_players() or player == None:
                    self.view.show_message("\nThis player doesn't exist :\n1) Try again \n2) Create a new player \n")
                    user_choice_option = self.view.get_input("Choose an option : ")
                    if user_choice_option == "1" or user_choice_option == "1)":
                        pass
                    elif user_choice_option == "2" or user_choice_option == "2)":
                        name = self.view.get_input("Name : ")
                        surname = self.view.get_input("Surname : ")
                        while True :
                            birthdate = self.view.get_input("Birthdate : ")
                            try:
                                from datetime import datetime
                                datetime.strptime(birthdate, "%d/%m/%Y")
                                break
                            except ValueError as e:
                                self.view.show_message(f"Invalid input: {e}")
                        
                        Player(national_chess_id, name, surname, birthdate).save_json()
                        #Tournament.add_player(tournament_id, national_chess_id)
                        Tournament.update_element(tournament_id, "players", [national_chess_id, 0.0])
                        self.view.show_message(f"\n{name} {surname} ({national_chess_id}) was successfully added !")
                
            elif user_choice == "2" or user_choice == "2)":
                break

    def play_tournament(self, tournament_id = None):
        
        tournaments = Tournament.get_all_tournaments()

        while tournament_id == None :
            self.view.show_message("\n[bold green]Play tournament[/bold green]\n")
            self.view.show_tournaments_list(tournaments)
            user_input = self.view.get_input("Select a tournament: ")
            if int(user_input) in tournaments :
                tournament_id = int(user_input)
            else :
                self.view.show_message("We didn't find any match, please try again")

        while True :
            tournaments = Tournament.get_all_tournaments()
            self.view.show_play_tournament_menu()
            user_input = self.view.get_input("\nSelect an option : ")
            if user_input == "1" or user_input == "1)" :
                self.round.create_round_menu(tournament_id)
            elif user_input == "2" or user_input == "2)" :
                pass
            elif user_input == "3" or user_input == "3)" :
                pass
            elif user_input == "4" or user_input == "4)" :
                break


class RoundController :
    
    def __init__(self, view):
        self.view = view

    def create_round_menu(self, tournament_id) :
        """
        Display the games of the new round
        """

        tournament_details = Tournament.get_tournament_details(tournament_id)
        current_round = tournament_details["current_round"]

        while True :
            if tournament_details["state"] == "not_started" :
                Tournament.update_element(tournament_id, "state", "in_progress")
            
            # Output selon l'etat du round :
            if current_round["state"] == "in_progress" :
                self.view.show_message("Please update the current round before to create a new one")
                break
            elif current_round["state"] == None or current_round["state"] == "finished"  :
                new_round = self.generate_round(tournament_details)
                Tournament.update_element(tournament_id, "current_round", {"round_number": current_round["round_number"] + 1, "state": "in_progress"})
                self.view.show_message(new_round)
                break

        
    def generate_round(self, tournament_id):
        """
        return a list new round for the tournament, based on actual players, score, and past rounds.

        Args :
            tournament : The tournament where to generate
        
        """
        
        def have_played_before(p1, p2, past_rounds):
            """
            return True if the two players have played in the past rounds on this tournament
            else return False 

            Args : 
                p1 and p2 : The two players
                past_rounds : The past rounds of the tournament
        
            """
            p1 = p1[0]
            p2 = p2[0]
            for rnd in past_rounds:
                for match in rnd:
                    if (p1 == match[0][0] and p2 == match[1][0]) or (p1 == match[1][0] and p2 == match[0][0]):
                        return True
            return False
            
        tournament_details = Tournament.get_tournament_details(tournament_id)
        players = tournament_details["players"]
        players.sort(key=lambda x: x[1])
        
        new_round = [] # liste des matchs du round
        used_players = []

        for player in players:
            if player in used_players:
                continue  # ce joueur est déjà apparié

            # chercher un adversaire
            for opponent in players:
                if opponent in used_players or opponent == player:
                    continue

                if have_played_before(player, opponent, tournament_details["rounds_list"]):
                    continue
                
                else :
                    new_round.append((player, opponent))
                    used_players.extend([player, opponent])
                    break # on passe au joueur suivant

            if player not in used_players :
                for opponent in players:
                    if opponent not in used_players and opponent != player:
                        new_round.append((player, opponent))
                        used_players.extend([player, opponent])
                        break

        Tournament.update_element(tournament_id, "rounds_list", new_round )
        return new_round
    







