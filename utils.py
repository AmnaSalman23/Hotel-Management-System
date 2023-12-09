# utils.py
from PyQt5.QtWidgets import QApplication, QMainWindow

class Utils:
    @staticmethod
    def open_login_page(database_manager):
        login_page = LoginPageUI(database_manager)
        login_page.show()

    @staticmethod
    def open_front_desk_landing_page(database_manager):
        front_desk_page = FrontDeskLandingPage(database_manager)
        front_desk_page.show()

    
