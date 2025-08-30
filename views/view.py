from rich import print


class View:    
    def get_input(self, input_user):
        self.input_user = input_user
        return input(input_user)

    def show_message(self, message):
        print(message)

    def main_menu(self):
        print("[bold green]\nMAIN MENU :\n[/bold green]")
        print("1) Manage tournaments")
        print("2) Manage players")
        print("3) Tournament reports")
        print("[red]4) Exit[/red]")

    def manage_tournaments_menu(self):
        print("\n[bold green]Manage tournaments[/bold green]\n")
        print("1) Create a tournament")
        print("2) Add players to a tournament")
        print("3) Play a tournament")
        print("4)[red] Back [/red]")

    def manage_players_menu(self):
        print("\n[bold green]Manage Players :[/bold green]\n")
        print("1) See all players")
        print("2) Add players")
        print("[red]3) Back [/red]")

    def add_players_tournament_menu(self):
        print("\n[bold green]Add players to a tournament[/bold green]")
        print("\n1) Add new players")
        print("2)[red] Back[/red]")



