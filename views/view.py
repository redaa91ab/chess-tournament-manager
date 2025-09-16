from rich import print

class View:    
    """
    A view class to display differents menu in the 
    application. 
    It displays menus, messages, and collects user input.
    """
    
    def get_input(self, message):
        """
        Prompt the user for input and return the entered value.

        Args:
            message : The prompt message to display

        Returns:
            The value entered by the user
        """
        self.message = message
        return input(message)

    def show_message(self, message):
        """
        Display a message

        Args:
            message : The message to display.
        """
        print(message)

    def show_main_menu(self):
        """
        Display the main menu.

        Shows options for managing tournaments, managing players, shows reports, or exit.
        """
        print("[bold green]\nMAIN MENU :\n[/bold green]")
        print("1) Manage tournaments")
        print("2) Manage players")
        print("3) Tournament reports")
        print("[red]4) Exit[/red]")

    def show_tournaments_menu(self):
        """
        Display the tournament management menu.

        Shows options for creating a tournament, adding players to a tournament, playing
        a tournament, or go back.
        """
        print("\n[bold green]Manage tournaments[/bold green]\n")
        print("1) Create a tournament")
        print("2) Add players to a tournament")
        print("3) Play a tournament")
        print("4)[red] Back [/red]")

    def show_manage_players_menu(self):
        """
        Display the player management menu.

        Shows options for viewing all players, adding new players, or going back.
        """

        print("\n[bold green]Manage Players :[/bold green]\n")
        print("1) See all players")
        print("2) Add players")
        print("[red]3) Back [/red]")

    def show_add_players_tournament_menu(self):
        """
        Display the menu for adding players to a tournament.

        Shows options for adding new players or going back.
        """
        print("\n1) Add new players")
        print("2)[red] Back[/red]")

    def show_play_tournament_menu(self):
        """
        Display the play tournament menu

        Show options
        """
        print("1) Continue ")
        print("2) Finish the tournament")
        print("3) [red] Back[/red]")



