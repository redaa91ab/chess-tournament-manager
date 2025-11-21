from rich.console import Console
from rich.tree import Tree
from rich.table import Table

console = Console()


class View:
    """
    A view class to display differents menu in the
    application.
    It displays menus, messages, and collects user input.
    """

    def get_input(self, message):
        """Prompt the user for input and return the value"""
        self.message = message
        return input(message)

    def show_message(self, message):
        """
        Display the message entered
        """
        console.print(message)

    def show_main_menu(self):
        """
        Display the main menu.

        Display options for managing tournaments, managing players, shows reports, or exit.
        """

        console.print("[bold green]\nMAIN MENU :\n[/bold green]")
        console.print("1) Manage tournaments")
        console.print("2) Manage players")
        console.print("3) Tournament reports")
        console.print("[red]4) Exit[/red]")

    def show_tournaments_menu(self):
        """
        Display the tournament management menu.

        Displays options for creating a tournament, add players to a tournament, play
        a tournament, or go back.
        """
        console.print("\n[bold green]Manage tournaments[/bold green]\n")
        console.print("1) Create a tournament")
        console.print("2) Add players to a tournament")
        console.print("3) Play a tournament")
        console.print("4)[red] Back [/red]")

    def show_manage_players_menu(self):
        """
        Display the player management menu.
        Displays options for display all players, adding new players, or going back
        """

        console.print("\n[bold green]Manage Players[/bold green]\n")
        console.print("1) See all players")
        console.print("2) Add players")
        console.print("[red]3) Back [/red]")

    def show_play_tournament_menu(self):
        """
        Display the play tournament menu
        Show options for create a new round, update the actual round, finish the tournament or go back
        """
        console.print("[bold green]Play Tournament[/bold green]")
        console.print("\n1) Create a new round ")
        console.print("2) Update results actual round")
        console.print("3) Finish the tournament")
        console.print("4)[red] Back[/red]")

    def show_select_tournament(self, tournaments):
        """Display all the tournaments and going back option"""

        tournament_table = Table(
            title="\n[bold green]\nTournaments[bold green]"
        )
        tournament_table.add_column("OPTION")
        tournament_table.add_column("NAME")
        tournament_table.add_column("START DATE")
        tournament_table.add_column("STATE")
        for i, tournament in enumerate(tournaments, 1):
            tournament_name = tournament.tournament_name
            start_date = tournament.start_date
            state = tournament.state
            tournament_table.add_row(
                str(i), tournament_name, start_date, state
            )

        console.print(tournament_table)
        console.print(f"{len(tournaments)+1})[red] Back[/red]")

    def show_games_list(self, round):
        """from a round, display all the games"""
        console.print(f"[bold green]\n{round.name}\n[/bold green]")

        games_list = round.games_list
        for i, game in enumerate(games_list, 1):
            player1 = game.player1_tournament
            player2 = game.player2_tournament
            console.print(
                f"{i}) {player1.name} ({player1.national_chess_id}) vs {player2.name} ({player2.national_chess_id})"
            )

    def update_game_result(self, round_name, game):
        """ask user winner of game and return the winner of the game"""
        console.print(f"[bold green]\n{round_name}\n[/bold green]")
        player1 = game.player1_tournament
        player2 = game.player2_tournament

        while True:
            console.print(f"{1}) {player1.name} ({player1.national_chess_id})")
            console.print("VS")
            console.print(f"{2}) {player2.name} ({player2.national_chess_id})")
            console.print("")
            console.print("3) Draw")

            user_choice = int(
                input("\n Select the winner (1 or 2) or draw (3) :")
            )
            if user_choice == 1:
                return player1
            elif user_choice == 2:
                return player2
            elif user_choice == 3:
                return None
            else:
                console.print("Please select an option between 1 and 3")

    def reports_menu(self):
        "Display the reports menu options"
        console.print("[bold green]\nREPORTS\n[/bold green]")
        console.print("1) Display all players")
        console.print("2) Display all tournaments")
        console.print("3)[red] Back[/red]")

    def reports_tournament_menu(self):
        "Display the tournament menu options"
        console.print("[bold green]\nTournament report\n[/bold green]")
        console.print("1) Display tournament players")
        console.print("2) Display tournament rounds and games")
        console.print("3)[red] Back[/red]")

    def display_players(self, players):
        "Display the players sorted by alphabetical order"
        players_sorted = sorted(players, key=lambda p: p.surname)
        table = Table(title="[bold green]\nPlayers[/bold green]")
        table.add_column("Surname", justify="center")
        table.add_column("Name", justify="center")
        table.add_column("National Chess ID", justify="center")
        table.add_column("Birthdate", justify="center")

        for player in players_sorted:
            table.add_row(
                player.surname,
                player.name,
                player.national_chess_id,
                player.birthdate,
            )

        console.print(table)

    def display_players_tournament(self, players):
        """Display all the players_tournament of a tournament, sorted by alphabetical order"""
        players_sorted = sorted(players, key=lambda p: p.surname)
        table = Table(title="[bold green]\nPlayers tournament[/bold green]")
        table.add_column("Surname", justify="center")
        table.add_column("Name", justify="center")
        table.add_column("National Chess ID", justify="center")
        table.add_column("Birthdate", justify="center")
        table.add_column("Total points", justify="center")

        for player in players_sorted:
            table.add_row(
                player.surname,
                player.name,
                player.national_chess_id,
                player.birthdate,
                str(player.total_points),
            )

        console.print(table)

    def display_tournament_rounds(self, tournament):
        """Display a tree of the games history of the tournament"""
        tree = Tree(f"[bold green]{tournament.tournament_name}[/bold green]\n")
        for round in tournament.rounds:
            round_tree = tree.add(f"[bold green]{round.name}[/bold green]\n")
            for game in round.games_list:
                player1 = game.player1_tournament
                player2 = game.player2_tournament
                game_tree = round_tree.add(
                    f"{player1.name} {player1.surname}({player1.national_chess_id})"
                    f" VS {player2.name} {player2.surname}({player2.national_chess_id})"
                )
                game_tree.add(f"Score {player1.name} : {game.score_player1}")
                game_tree.add(f"Score {player2.name} : {game.score_player2}\n")
        console.print("\n", tree)

    def display_rank_players(self, tournament):
        """Display all players of a tournament sorted from highest to lowest total score"""
        players_sorted = sorted(
            tournament.players,
            key=lambda player: player.total_points,
            reverse=True,
        )
        table = Table(title="[bold green]Players rank[/bold green]")
        table.add_column("Rank place", justify="center")
        table.add_column("Player", justify="center")
        table.add_column("Total points", justify="center")

        for i, player in enumerate(players_sorted, 1):
            table.add_row(
                str(i),
                (
                    f"{player.name} {player.surname} ({player.national_chess_id})"
                ),
                str(player.total_points),
            )

        console.print("\n", table)
