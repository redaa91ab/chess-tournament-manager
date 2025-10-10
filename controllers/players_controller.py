from models import Player

class PlayersController: 
    """
    A controller class for managing player. 
    It provides methods to display all the players and adding new players to the database
    """

    def __init__(self, view, parent = None):
        """
        Initialize a PlayersController instance.

        Args:
            view: An instance of the View class
            parent: app_controller.py
        """
        self.view = view
        self.parent = parent

    def display_all_players(self):
        """
        Display the list of all players using the method return_players of the Player model.
        """
        self.view.show_message(Player.get_all_players())

    def add_player(self) :
        """ 
        Collect the player details, then use the methods save_json of the Player model.
        """

        self.view.show_message("\nEnter the new player details below :")
        national_chess_id = self.view.get_input("National chess ID : ")
        player = Player.get_player_details(national_chess_id)
        if player :
            self.view.show_message("This player already exist")
        elif player == None :
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

            self.view.show_message(f"\n{name} {surname} ({national_chess_id}) was successfully added !")
            player = Player(national_chess_id, name, surname, birthdate)
            player.save_json()
