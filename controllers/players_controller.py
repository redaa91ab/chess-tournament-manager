from models import Player
from datetime import datetime
import re


class PlayersController:
    """
    A controller class for managing player.
    It provides methods to show manage players menu to display the players and add new players to the database
    """

    def __init__(self, view):
        """
        Initialize a PlayersController instance.

        Args:
            view: View class instance
        """
        self.view = view

    def manage_players(self):
        """Display the player management menu, and direct the tasks to the other methods"""
        while True:
            self.view.show_manage_players_menu()
            user_choice = self.get_valid_choice(3)
            if user_choice == 1:
                self.display_all_players()
            elif user_choice == 2:
                self.add_player()
            elif user_choice == 3:
                break

    def display_all_players(self):
        """Display the list of all players using the deserialize_all_players method of the Player model"""
        players = Player.deserialize_all_players()
        self.view.display_players(players)

    def add_player(self, national_chess_id=None):
        """
        Collect the player details, then use the save_json method of the Player model.
        """

        self.view.show_message("\nEnter the new player details below :")
        if national_chess_id is None:
            national_chess_id = self.get_valid_national_chess_id()

        player = Player.deserialize(national_chess_id)
        if player:
            self.view.show_message(
                f"{player.name} ({national_chess_id}) is already saved in the database !"
            )
        elif player is None:
            name = self.view.get_input("Name : ")
            surname = self.view.get_input("Surname : ")
            birthdate = self.get_valid_birthdate()
            player = Player(national_chess_id, name, surname, birthdate)
            player.save_json()
            self.view.show_message(
                f"\n{name} {surname} ({national_chess_id}) was successfully added to the database !"
            )
            return player

    def get_valid_choice(self, number_of_choice):
        """return a valid choice number between the range of the number of choice"""
        while True:
            try:
                user_choice = int(self.view.get_input("\nSelect an option : "))
                if 1 <= user_choice <= number_of_choice:
                    return user_choice
                else:
                    self.view.show_message("Please select a valid option")
            except ValueError:
                self.view.show_message("Please enter a number")

    def get_valid_national_chess_id(self):
        """Return a valid national chess id"""

        while True:
            input = self.view.get_input("National chess ID: ")
            if re.match(r"^[A-Za-z]{2}\d{5}$", input):
                national_chess_id = input
                return national_chess_id
            else:
                self.view.show_message(
                    "The ID should start with 2 letters and 5 numbers. Try again"
                )

    def get_valid_birthdate(self):
        """Return a valid birthdate"""
        while True:
            birthdate = self.view.get_input("Birthdate : ")
            try:
                datetime.strptime(birthdate, "%d/%m/%Y")
                return birthdate
            except ValueError as e:
                self.view.show_message(f"Invalid input: {e}")
