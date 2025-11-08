from rich.console import Console
from rich.table import Table
console = Console()

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

        console.print("[bold green]\nMAIN MENU :\n[/bold green]")
        console.print("1) Manage tournaments")
        console.print("2) Manage players")
        console.print("3) Tournament reports")
        console.print("[red]4) Exit[/red]")

    def show_tournaments_menu(self):
        """
        Display the tournament management menu.

        Shows options for creating a tournament, adding players to a tournament, playing
        a tournament, or go back.
        """
        console.print("\n[bold green]Manage tournaments[/bold green]\n")
        console.print("1) Create a tournament")
        console.print("2) Add players to a tournament")
        console.print("3) Start a tournament")
        console.print("4)[red] Back [/red]")

    def show_manage_players_menu(self):
        """
        Display the player management menu.

        Shows options for viewing all players, adding new players, or going back.
        """

        console.print("\n[bold green]Manage Players :[/bold green]\n")
        console.print("1) See all players")
        console.print("2) Add players")
        console.print("[red]3) Back [/red]")

    def show_add_players_tournament_menu(self, tournament):
        """
        Display the menu for adding players to a tournament.

        Shows options for adding new players or going back.
        """
        console.print(f"[bold green]\n{tournament.tournament_name}[/bold green]")
        console.print("\n1) Add new player")
        console.print("2)[red] Back[/red]")

    def show_start_tournament_menu(self):
        """
        Display the start tournament menu

        Show options
        """
        console.print("[bold green]\Start Tournament[/bold green]")
        console.print("\n1) Create a new round ")
        console.print("2) Update the actual round")
        console.print("3) Finish the tournament")
        console.print("4)[red] Back[/red]")

    def show_tournaments_list(self, tournaments):
        print("[bold green]\nAll tournaments\n[/bold green]")

        tournament_table = Table(title="Tournaments")
        tournament_table.add_column("NUMBER")
        tournament_table.add_column("NAME")
        tournament_table.add_column("DATE")
        tournament_table.add_column("STATE")
        for i, tournament in enumerate(tournaments, 1):
            tournament_name = tournament.tournament_name
            start_date = tournament.start_date
            state = tournament.state
            tournament_table.add_row(str(i), tournament_name, start_date, state)
            #console.print(f"[bold cyan]{i}.[/] {tournament_name} ({start_date}) | [yellow]{state}[/]")
        #console.print(f"{len(tournaments)+1}.[red] Back[/red]")
        
        console.print(tournament_table)
        console.print("3)[red] Back[/red]")

    def show_games_list(self, round):
        console.print("[bold green]\nGames\n[/bold green]")

        games_list = round.games_list
        for i, game in enumerate(games_list, 1) :
            player1 = game.player1.player
            player2 = game.player2.player
            console.print(f"{i}) {player1.name} ({player1.national_chess_id}) vs {player2.name} ({player2.national_chess_id})")

    
    def update_game_result(self, game) :
        """return the winner of the game"""
        console.print("[bold green]\nUpdate game\n[/bold green]")
        player1 = game.player1
        player2 = game.player2

        while True :
            console.print(f"{1}) {player1.player.name} ({player1.player.national_chess_id})")
            console.print("VS")
            console.print(f"{2}) {player2.player.name} ({player2.player.national_chess_id})")
            console.print("")
            console.print("3) Draw")
        
            user_choice = int(input(f"\n Enter the number of the winner (1 or 2) or draw (3) :"))
            if user_choice == 1 :
                return player1
            elif user_choice == 2 :
                return player2
            elif user_choice == 3 :
                return None
            else :
                console.print("Please choose a choice between 1 and 3")

    def reports_menu(self):
        "Display the reports menu"
        console.print("[bold green]\nREPORTS\n[/bold green]")
        console.print("1) Display all players")
        console.print("2) Display all tournaments")
        console.print("3)[red] Back[/red]")

    def display_all_players(self, players) :
        table = Table(title="Players")
        table.add_column("National Chess ID", justify="center")
        table.add_column("Name", justify="center")
        table.add_column("Surname", justify="center")
        table.add_column("Birthdate", justify="center")

        for player in players :
            table.add_row(player.national_chess_id, player.name, player.surname, player.birthdate)

        console.print(table)






            




