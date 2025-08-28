from rich import print


class View:    
    def get_input(self, input_user):
        self.input_user = input_user
        return input(input_user)

    def show_message(self, message):
        print(message)


class MainMenu(View) :
    def show(self):
        print("[bold green]\nMAIN MENU :\n[/bold green]")
        print("1) Start")
        print("2) Manage players")
        print("3) Tournament reports")
        print("[red]4) Exit[/red]")

class StartMenu(View):
    def show(self):
        print("\n[bold green]Start[/bold green]\n")
        print("1) Create a new tournament")
        print("2) Choose an existing tournament")
        print("3)[red] Back [/red]")

class NewTournamentMenu(View) :
    def show(self):
        print("\n[bold green]New tournament[/bold green]")
        print("\n1) Add new players")
        print("2)[red] Back[/red]")


class ManagePlayersMenu(View):
    def show(self):
        print("\n[bold green]Manage Players :[/bold green]\n")
        print("1) See all players")
        print("2) Add players")
        print("[red]3) Back [/red]")


