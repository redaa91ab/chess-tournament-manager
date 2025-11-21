"""Main entry for the chess tournament management application."""

from controllers import AppController

if __name__ == "__main__":
    app_controller = AppController()
    app_controller.run()
