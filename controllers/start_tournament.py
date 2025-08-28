from models import *
from views import *
from rich import print


class StartTournament:
    def __init__(self, parent):
        self.view = View()
        self.start_menu = StartMenu()
        self.parent = parent
        

    def start(self):


        self.start_menu.show()   
        input_live = self.view.get_input("\nChoose an option : ")
        while input_live == "1" or input_live == "1)": 
            self.parent.run_new_tournament()

        while input_live == "2" or input_live == "2)":
            pass

        while input_live == "3" or input_live == "3)":   
            self.parent.run()
