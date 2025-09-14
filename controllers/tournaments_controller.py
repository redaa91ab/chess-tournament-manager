from models import Tournament, Player
from rich import print


class TournamentsController:
    """
    A controller class for managing tournament.
    It provides methods to create a new tournament in tournaments.json and add new players to a tournament
    """

    def __init__(self,view, parent = None):
        """
        Initialize a TournamentsController instance.

        Args:
            view: An instance of the View class
            parent : app_controller.py
        """
        self.parent = parent
        self.view = view

    def create(self):
        """
        Collect new tournament details and save it in tournaments.json by using the methods save_json of the model Tournament
        """
        self.view.show_message("\n[bold green]New tournament[/bold green]\n")
        self.view.show_message("Enter the new tournament details below : ")
        tournament_name = self.view.get_input("Tournament name : ").upper()
        place = self.view.get_input("Place : ")
        start_date = self.view.get_input("Start date (DD/MM/YYYY) : ")
        end_date = self.view.get_input("End date (DD/MM/YYYY): ")
        number_of_rounds = self.view.get_input("Number of rounds : ")

        try:
            if Tournament.get_tournament_details(tournament_name) != None :
                raise ValueError("This tournament name is already taken")
            
            number_of_rounds = int(number_of_rounds)
            from datetime import datetime
            datetime.strptime(start_date, "%d/%m/%Y")
            datetime.strptime(end_date, "%d/%m/%Y")
        except ValueError as e:
            self.view.show_message(f"Invalid input: {e}")
            return

        tournament = Tournament(tournament_name, place, start_date, end_date, number_of_rounds)
        tournament.save_json()
        self.add_player_tournament(tournament.tournament_name)

    def add_player_tournament(self, tournament_name = None):
        """
        Add players to a tournament in tournaments.json

        Args:
            tournament_name : The name of the tournament to add players to.
                              If None, prompts the user to enter a tournament name.

        Collect the tournament name if not provided and add player to the tournament in tournaments.json.
        If a player doesn't exist, offers the option to create a new player or try again.
        """
        while tournament_name == None :
            user_input = self.view.get_input("\nEnter the tournament name : ")
            user_input = user_input.upper() 
            if Tournament.get_tournament_details(user_input) == None :
                self.view.show_message("We didn't find any match, please try again")
            else :
                tournament_name = user_input

        self.view.show_message(f"[bold green]\n{tournament_name}[/bold green]")
        self.view.show_add_players_tournament_menu()
        user_choice = self.view.get_input("\nChoose an option : ")

        while user_choice == "1" or user_choice == "1)":
            self.view.show_message(f"\n[bold green]\n{tournament_name}[/bold green]\n")
            national_chess_id = self.view.get_input("Add a player (National Chess ID) : ")
            player = Player.get_player_details(national_chess_id)
            if player == None :
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
                    Tournament.add_player(tournament_name, national_chess_id)
                    self.view.show_message(f"\n{name} {surname} ({national_chess_id}) was successfully added !")
                    self.add_player_tournament(tournament_name)
            else :
                Tournament.add_player(tournament_name, national_chess_id)
                self.view.show_message(f"\n{player["Name"]} {player["Surname"]} ({player["National chess ID"]}) was successfully added !")
                self.add_player_tournament(tournament_name)

        while user_choice == "2" or user_choice == "2)":
            self.parent.manage_tournaments()


    
    def generate_round(tournament):
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
            
        tournament = Tournament.get_tournament_details(tournament)
        players = tournament["Players"]
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

                if have_played_before(player, opponent, tournament["Rounds list"]):
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
        return new_round
    
    def play_tournament(tournament):
        rounds_list = tournament["Rounds list"]
        def is_round_finished(actual_round, players):
            for game in actual_round :
                for player in game :
                    if player != players[player][] :
                        return False
        
        return is_round_finished(rounds_list[1], rounds_list[2])
    






