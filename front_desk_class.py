from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem
import time
import pyqtgraph as pg
import numpy as np
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon
from database import create_database
from customer_landing_page import Ui_MainWindow as cust
# from admin_landing_page import Ui_MainWindow as admin
from front_desk import Ui_MainWindow as front
from show_messages import show_error_message, show_success_message
# from login_page_class import LoginPageUI

class FrontDeskLandingPage(QMainWindow):
    def __init__(self, database_manager):
        super().__init__()
        self.database_manager = database_manager
        # Create an instance of the generated UI class
        self.ui = front()
        self.ui.setupUi(self)
        self.sidebar_visible = False
        self.ui.dashboardBtn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Dashboard_2))
        self.ui.checkInPageBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.checkInPage))
        self.ui.checkOutBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.checkOutPage))
        self.ui.guestServicePageBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.servicePage))
        self.ui.reservationPageBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.reservationPage))
        self.ui.userProfileBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.userProfilePage))
        self.ui.logoutBtn.clicked.connect(self.open_login_page)
        self.ui.guestFirstNameInput.setPlaceholderText("First Name")
        self.ui.guestLastName.setPlaceholderText("Last Name")
        self.ui.guestEmail.setPlaceholderText("Email")
        self.ui.guestPhoneNumber.setPlaceholderText("Phone Number")
        self.ui.guestAdress.setPlaceholderText("Address")
        self.ui.customerNameInput.setPlaceholderText("Guest Name")
        self.ui.guestNameInput.setPlaceholderText("Guest Name")
        self.ui.guestNameInput_2.setPlaceholderText("Guest Name")
        self.ui.selectedServiceQuantity.setPlaceholderText("Quantity")
        self.ui.userProfileName.setPlaceholderText("Guest Name")
        self.ui.userProfilePassword.setPlaceholderText("Password")
        self.ui.navBar_2.clicked.connect(self.toggle_sidebar)
        self.show_all_guests()
    def open_login_page(self):
        self.login_form = LoginPageUI(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.login_form.show()
    def toggle_sidebar(self):
        # Toggle the sidebar visibility
        self.sidebar_visible = False if self.sidebar_visible else True
        self.animate_sidebar()
    
    def animate_sidebar(self):

        self.ui.dashboardBtn_2.setText("Dashboard" if self.sidebar_visible else "")
        self.ui.checkInPageBtn.setText("CheckIn" if self.sidebar_visible else "")
        self.ui.checkOutBtn.setText("Checkout" if self.sidebar_visible else "")
        self.ui.guestServicePageBtn.setText("Guest Services" if self.sidebar_visible else "")
        self.ui.userProfileBtn.setText("User Profile" if self.sidebar_visible else "")
        # self.ui.checkOutBtn.setText("Backup" if self.sidebar_visible else "")
        self.ui.label_2.setText("InnSync" if self.sidebar_visible else "Inn\nSync")
        self.ui.reservationPageBtn.setText("Reservation" if self.sidebar_visible else "")
        # self.ui.roomAssignmentPageBtn.setText("Assign Room" if self.sidebar_visible else "")
        self.ui.logoutBtn.setText("Logut" if self.sidebar_visible else "")
        self.ui.navBar_2.setIcon(QIcon(QPixmap("images/icons8-close-128.png").scaled(60,60)) if self.sidebar_visible else QIcon("images/icons8-hamburger-100.png"))
        if self.sidebar_visible:
            time.sleep(0.2)
            self.ui.frame.setFixedWidth(250)
        else:
            time.sleep(0.2)
            self.ui.frame.setFixedWidth(100)
        

    def add_guest(self):
        # For example:
        first_name = self.ui.guestFirstNameInput
        last_name = self.ui.guestLastName
        email = self.ui.guestEmail
        phone_number = self.ui.guestPhoneNumber
        address = self.ui.guestAdress
        # Insert the guest into the Guests table
        self.database_manager.insert_guest(first_name, last_name, email, phone_number, address)

    def show_all_guests(self):
        # Assuming self.database_manager.fetch_all() returns a list of tuples
        sample_data = self.database_manager.fetch_all("SELECT * FROM Guests")
        
        # Clear existing data in the table
        self.ui.showAllUsersTable.setRowCount(0)

        if len(sample_data) > 0:
            # Set the number of rows and columns in the table
            self.ui.showAllUsersTable.setRowCount(len(sample_data))
            self.ui.showAllUsersTable.setColumnCount(len(sample_data[0]))

            # Populate the table with data
            for row_num, row_data in enumerate(sample_data):
                for col_num, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.ui.showAllUsersTable.setItem(row_num, col_num, item)

        else:
            # If there is no data, set columns to 0
            self.ui.showAllUsersTable.setColumnCount(0)