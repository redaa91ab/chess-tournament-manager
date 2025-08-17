from rich import print


class View:
    def show_menu(self):
        print("[bold green]\nMAIN MENU :\n[/bold green]")
        print("1) New tournament")
        print("2) Load tournament")
        print("3) Manage players")
        print("4) Tournament reports")
        print("[red]5) Exit[/red]")
    
    def get_input(self, input_user):
        self.input_user = input_user
        return input(input_user)

    def show_message(self, message):
        self.message = message
        print(self.message)