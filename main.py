import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from landing_page import Ui_MainWindow  # Import the generated UI class
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QObject, pyqtSignal
from loginPage import Ui_MainWindow as logi
from SignUpForm import Ui_MainWindow as sign
import time
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QSize
from PyQt5.QtGui import QIcon
from database import create_database
from customer_landing_page import Ui_MainWindow as cust
from admin_landing_page import Ui_MainWindow as admin
import sqlite3
import os



# Global Variables
LoggedUserName=""
LoggedUserType=""
LoggedUserPassword=""

def show_error_message(self, message):
    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Critical)
    error_dialog.setText(message)
    error_dialog.setWindowTitle("Error")
    error_dialog.exec_()

class DatabaseManager:
    def __init__(self, database_name):
        self.database_name = database_name

    def __enter__(self):
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def execute_query(self, query, values=None):
        with self:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            self.connection.commit()

    def fetch_one(self, query, values=None):
        with self:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()

    def fetch_all(self, query, values=None):
        with self:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        
    def register_user(self, username, password, email, user_type):
        query = '''
            INSERT INTO Users (Username, Password, Email, UserType)
            VALUES (?, ?, ?, ?)
        '''
        try:
            self.execute_query(query, (username, password, email, user_type))
            return True  # Successful registration
        except sqlite3.IntegrityError:
            return False  # User with the same username or email already exists
    def get_user_role(self, username, password):
        query = '''
            SELECT UserType
            FROM Users
            WHERE Users.Username = ? AND Users.Password = ?
        '''
        result = self.fetch_one(query, (username, password))
        if result:
            return result[0]
        return None



class LoginPageUI(QMainWindow):
    def __init__(self,database_manager):
        super().__init__()
        self.database_manager = database_manager
        self.current_user_id = None
        # Create an instance of the generated UI class
        self.ui = logi()
        self.ui.setupUi(self)

        # self.ui.pushButton_2.clicked.connect(self.logn_successful)
        self.ui.showPasswordBtn.clicked.connect(self.show_password)
        # self.ui.pushButton_4.clicked.connect(self.open_signup_page)
        self.ui.loginBtn.clicked.connect(self.logn_successful)
        self.ui.userNameInput.mousePressEvent = self.clear_username
        self.ui.userPasswordInput.mousePressEvent = self.clear_password
        self.ui.userNameInput.setPlaceholderText("UserName")
        self.ui.userPasswordInput.setPlaceholderText("Password")
        self.ui.userPasswordInput.setEchoMode(2)
        

 


        # self.ui.userPasswordInput.setEchoMode(2)
    
    def clear_username(self, event):
        if self.ui.userNameInput.text() == "UserName":
            self.ui.userNameInput.setText("")
        
    def clear_password(self, event):
        if self.ui.userPasswordInput.text() == "Password":
            self.ui.userPasswordInput.setText("")
            self.ui.userPasswordInput.setEchoMode(2)

    def show_password(self):
        if self.ui.showPasswordBtn.isChecked():
            self.ui.userPasswordInput.setEchoMode(0)
        else:
            if self.ui.userPasswordInput.text() != "Password":
                self.ui.userPasswordInput.setEchoMode(2)
            # self.ui.userPasswordInput.setEchoMode(2)

    
    def open_signup_page(self):
        self.signup_form = SignUpPageUI()
        self.hide()
        time.sleep(0.2)
        self.signup_form.show()

    # def logn_successful(self):
    #     if self.ui.lineEdit.text() == "admin" and self.ui.lineEdit_2.text() == "admin":
    #         self.open_landing_page()
    #     # self.open_landing_page

    def open_landing_page(self):
        self.landing_form = MainUIClass()
        self.hide()
        time.sleep(0.2)
        self.landing_form.show()

    
    def logn_successful(self):
        try:
            username = self.ui.userNameInput.text()
            global LoggedUserName
            LoggedUserName=username
            global LoggedUserPassword
            LoggedUserPassword=self.ui.userPasswordInput.text()
            password = self.ui.userPasswordInput.text()
            print(username, password)
            user_role = self.database_manager.get_user_role(username, password)  # Implement this function
            print(user_role)
            if user_role == "Admin" or user_role == "admin":
                self.open_admin_landing_page()
            elif user_role == "Manager" or user_role == "manager":
                self.open_manager_landing_page()
            elif user_role == "Staff" or user_role == "staff":
                self.open_staff_landing_page()
            elif user_role == "Customer" or user_role == "customer":
                self.open_customer_landing_page()
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            show_error_message(self, f"An error occurred: {str(e)}")

    def open_admin_landing_page(self):
        self.landing_form = AdminLandingPage()
        self.hide()
        time.sleep(0.2)
        self.landing_form.show()

    def open_manager_landing_page(self):
        self.landing_form=MainUIClass()
        self.hide()
        time.sleep(0.2)
        self.landing_form.show()

    def open_staff_landing_page(self):
        # Open the staff landing page
        pass

    def open_customer_landing_page(self):
        self.landing_form = CustomerLandingPage()
        self.hide()
        time.sleep(0.2)
        self.landing_form.show()

   
    
class SignUpPageUI(QMainWindow):
    def __init__(self,database_manager):
        super().__init__()
        self.database_manager = database_manager
        # Create an instance of the generated UI class
        self.ui = sign()
        self.ui.setupUi(self)

        self.ui.loginBtn.clicked.connect(self.open_login_page)
        self.ui.showPasswordBtn.clicked.connect(self.show_password)
        # self.ui.pushButton_4.clicked.connect(self.open_login_page)
        self.ui.userNameInput.mousePressEvent = self.clear_username
        self.ui.userPasswordInput.mousePressEvent = self.clear_password
        self.ui.userPasswordInput_2.mousePressEvent = self.clear_confirmPassword
        self.ui.signUpBtn.clicked.connect(self.store_signup_data)
        self.ui.userEmailInput.mousePressEvent = self.clear_email
        self.ui.userNameInput.setPlaceholderText("UserName")
        self.ui.userPasswordInput.setPlaceholderText("Password")
        self.ui.userPasswordInput_2.setPlaceholderText("Confirm Password")
        self.ui.userEmailInput.setPlaceholderText("Email")
        
        self.ui.userPasswordInput.setEchoMode(2)
        self.ui.userPasswordInput_2.setEchoMode(2)

    def store_signup_data(self):
        username = self.ui.userNameInput.text()
        password = self.ui.userPasswordInput.text()
        confirm_password = self.ui.userPasswordInput_2.text()
        email = self.ui.userEmailInput.text()
        user_role = "Customer"

        if password == confirm_password:
            # Check if the user with the same username or email already exists
            if not self.database_manager.user_exists(username, email):
                # Register the user
                if self.database_manager.register_user(username, password, email, user_role):
                    self.signup_successful()
                else:
                    show_error_message(self, "Error: Failed to register user.")
            else:
                show_error_message(self, "Error: User with the same username or email already exists.")
        else:
            show_error_message(self, "Error: Passwords do not match.")

    def signup_successful(self):
        customer= CustomerLandingPage()
        self.hide()
        customer.show()  # Pass the database_manager to LoginPageUI

    def open_login_page(self, database_manager):
        self.login_form = LoginPageUI(database_manager)
        self.hide()
        time.sleep(0.2)
        self.login_form.show()

    def show_password(self):
        if self.ui.showPasswordBtn.isChecked():
            self.ui.userPasswordInput.setEchoMode(0)
            self.ui.userPasswordInput_2.setEchoMode(0)
        else:
            self.ui.userPasswordInput.setEchoMode(2)
            self.ui.userPasswordInput_2.setEchoMode(2)
            # self.ui.userPasswordInput.setEchoMode(2)
    def clear_email(self, event):
        if self.ui.userEmailInput.text() == "Email":
            self.ui.userEmailInput.setText("")

    def clear_username(self, event):
        if self.ui.userNameInput.text() == "UserName":
            self.ui.userNameInput.setText("")
    
    def clear_password(self, event):
        if self.ui.userPasswordInput.text() == "Password":
            self.ui.userPasswordInput.setText("")
            self.ui.userPasswordInput.setEchoMode(2)
    
    def clear_confirmPassword(self, event):
        if self.ui.userPasswordInput_2.text() == "Confirm Password":
            self.ui.userPasswordInput_2.setText("")
            self.ui.userPasswordInput.setEchoMode(2)
    
    def open_login_page(self):
        self.login_form = LoginPageUI()
        self.hide()
        time.sleep(0.2)
        self.login_form.show()

    # def signup_successful(self):
    #     self.open_login_page()
    #     # self.open_landing_page

    def store_signup_data(self):
        username = self.ui.userNameInput.text()
        password = self.ui.userPasswordInput.text()
        confirm_password = self.ui.userPasswordInput_2.text()
        email = self.ui.userEmailInput.text()
        user_role = "Customer"

        if password == confirm_password:
            self.store_user_data(username, password, email, user_role)
            self.signup_successful()
        else:
            print("Could not sign up")
            show_error_message("Passwords do not match")
        
    

    def store_user_data(self, username, password, email, user_role):
        query = '''
            INSERT INTO Users (Username, Password, Email, UserType)
            VALUES (?, ?, ?, ?)
        '''
        self.database_manager.execute_query(query, (username, password, email, user_role))
       
    
class MainUIClass(QMainWindow):
    def __init__(self, database_manager):
        super().__init__()
        self.database_manager = database_manager
        # Create an instance of the generated UI class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.dashboardBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Dashboard))
        
        # PAGE 2 Settings Page
        self.ui.manageUsersBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.manageStaffPage))
        
        self.ui.manageServicesBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.manageServicePage))
        
        self.ui.manageBookingBtn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.manageBookingPage))
        self.ui.profilePageBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.userProfile))
        self.ui.managePaymentsBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.managePaymentsPage))

        self.ui.addUserBtn.clicked.connect(self.add_user)
        self.ui.navBar.clicked.connect(self.toggle_sidebar)
        self.loadAllEmployeesGraph()

        self.ui.userNameInput.setPlaceholderText("Name")
        self.ui.userEmail.setPlaceholderText("Email")
        self.ui.userPasswordInput.setPlaceholderText("Password")
        self.populate_table_with_sample_data()
        

        # Initialize sidebar state (visible)
        self.sidebar_visible = False
        

    def add_user(self):
        try:
            username = self.ui.userNameInput.text()
            password = self.ui.userPasswordInput.text()
            email = self.ui.userEmail.text()
            # user_role = self.ui.userRoleInput.currentText()
            user_role = "Staff"

            success = self.database_manager.register_user(username, password, email, user_role)

            if success:
                show_error_message(self, "User added successfully")
                self.populate_table_with_sample_data()
            else:
                show_error_message(self, "Error: Failed to register user.")
        except Exception as e:
            print(f"An error occurred during user registration: {str(e)}")
            show_error_message(self, f"An error occurred during user registration: {str(e)}")
    
    def populate_table_with_sample_data(self):
        try:
            # Fetch all users from the database
            sample_data = self.database_manager.fetch_all("SELECT * FROM Users Where UserType='Staff'")

            # Set the number of rows and columns
            self.ui.showAllUsers.setRowCount(len(sample_data))
            if len(sample_data) > 0:
                self.ui.showAllUsers.setColumnCount(len(sample_data[0]))
            else:
                self.ui.showAllUsers.setColumnCount(0)

            # Insert data into the table
            for row_idx, row_data in enumerate(sample_data):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.ui.showAllUsers.setItem(row_idx, col_idx, item)

        except Exception as e:
            print(f"An error occurred while populating the table: {str(e)}")
            show_error_message(self, f"An error occurred while populating the table: {str(e)}")
    
    def on_button_click(self):
        # Define what happens when the button is clicked
        self.ui.label.setText("Button Clicked!")

    def loadAllEmployeesGraph(self):
        employees = ["Manager", "Sales Agent", "Order Dispatcher", "Delivery Man"]
        num = [10, 200, 40, 30]
        colors = ['#8CDBA9', '#4E9C81', '#49DCB1', '#00917C']

        # Set the figsize to 300x300
        plt.figure(figsize=(1, 1), dpi=10)

        explode = (0, 0.1, 0, 0)
        fig1, ax1 = plt.subplots()
        ax1.pie(num, explode=explode, labels=employees, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')

        # Save the figure with a specific dpi
        plt.savefig("allEmployeesGraph.png", transparent=True, dpi=50)

        pixmap = QPixmap('allEmployeesGraph.png')
        self.ui.lblSalePerDay.setPixmap(pixmap)
        self.ui.lblSalePerDay_2.setPixmap(pixmap)

    def toggle_sidebar(self):
        # Toggle the sidebar visibility
        self.sidebar_visible = False if self.sidebar_visible else True
        self.animate_sidebar()

    def animate_sidebar(self):
        # Toggle the sidebar visibility
        # self.sidebar_visible = not self.sidebar_visible
        self.ui.dashboardBtn.setText("Dashboard" if self.sidebar_visible else "")
        self.ui.manageUsersBtn.setText("Manage Staff" if self.sidebar_visible else "")
        self.ui.manageServicesBtn.setText("Services" if self.sidebar_visible else "")
        self.ui.manageBookingBtn_2.setText("Booking" if self.sidebar_visible else "")
        # self.ui.navBar.setText(">" if self.sidebar_visible else "<")
        self.ui.managePaymentsBtn.setText("Payments" if self.sidebar_visible else "")
        self.ui.label.setText("InnSync" if self.sidebar_visible else "Inn\nSync")
        # self.ui.pushButton.setFixedWidth(50 if self.sidebar_visible else 0)
        
        self.ui.navBar.setIcon(QIcon(QPixmap("images/icons8-close-128.png").scaled(60,60)) if self.sidebar_visible else QIcon("images/icons8-hamburger-100.png"))

        # Update the width of the frame based on sidebar visibility
        if self.sidebar_visible:
            time.sleep(0.2)
            self.ui.frame.setFixedWidth(250)
        else:
            time.sleep(0.2)
            self.ui.frame.setFixedWidth(100)

class CustomerLandingPage(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create an instance of the generated UI class
        self.ui = cust()
        self.ui.setupUi(self)

        # elf.ui.pushButton_2.clicked.connect(self.open_login_page)
        # self.ui.pushButton_4.clicked.connect(self.open_signup_page)s

        self.ui.dashboardBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Dashboard))
        self.ui.bookRoomBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.bookRoomPage))
        # self.ui.manageBookingBtn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.manageBookingPage))
        self.ui.profilePageBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.userProfile))
        self.ui.managePaymentsBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.managePaymentsPage))
        self.ui.navBar.clicked.connect(self.toggle_sidebar)


    def toggle_sidebar(self):
        # Toggle the sidebar visibility
        self.sidebar_visible = False if self.sidebar_visible else True
        self.animate_sidebar()

    def animate_sidebar(self):
        # Toggle the sidebar visibility
        # self.sidebar_visible = not self.sidebar_visible
        self.ui.dashboardBtn.setText("Dashboard" if self.sidebar_visible else "")
        self.ui.manageUsersBtn.setText("Manage Staff" if self.sidebar_visible else "")
        self.ui.manageServicesBtn.setText("Services" if self.sidebar_visible else "")
        self.ui.manageBookingBtn_2.setText("Booking" if self.sidebar_visible else "")
        # self.ui.navBar.setText(">" if self.sidebar_visible else "<")
        self.ui.managePaymentsBtn.setText("Payments" if self.sidebar_visible else "")
        self.ui.label.setText("InnSync" if self.sidebar_visible else "Inn\nSync")
        # self.ui.pushButton.setFixedWidth(50 if self.sidebar_visible else 0)
        
        self.ui.navBar.setIcon(QIcon(QPixmap("images/icons8-close-128.png").scaled(60,60)) if self.sidebar_visible else QIcon("images/icons8-hamburger-100.png"))

        # Update the width of the frame based on sidebar visibility
        if self.sidebar_visible:
            time.sleep(0.2)
            self.ui.frame.setFixedWidth(250)
        else:
            time.sleep(0.2)
            self.ui.frame.setFixedWidth(100)

    def open_login_page(self):
        self.login_form = LoginPageUI()
        self.hide()
        time.sleep(0.2)
        self.login_form.show()

    def open_signup_page(self):
        self.signup_form = SignUpPageUI()
        self.hide()
        time.sleep(0.2)
        self.signup_form.show()



class AdminLandingPage(QMainWindow):
    def __init__(self, database_manager):
        super().__init__()
        self.database_manager = database_manager
        # Create an instance of the generated UI class
        self.ui = admin()
        self.ui.setupUi(self)

        # Connect button signals
        self.ui.addUserBtn.clicked.connect(self.add_user)

        # Set placeholders
        self.ui.userNameInput.setPlaceholderText("UserName")
        self.ui.userPasswordInput.setPlaceholderText("Password")
        self.ui.userEmailInput.setPlaceholderText("Email")
        self.ui.userRoleInput.setPlaceholderText("Role")
        self.ui.userProfileName.setPlaceholderText("Name")
        self.ui.userProfilePassword.setPlaceholderText("Password")
        self.ui.manageStaffBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.manageStaffPage))
        self.ui.userProfileBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.userProfilePage))
        self.ui.dashboardBtn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Dashboard_2))

        self.ui.userProfileName=LoggedUserName
        self.ui.userProfilePassword=LoggedUserPassword

        # Add sample data to the table
        self.populate_table_with_sample_data()

    def populate_table_with_sample_data(self):
        try:
            # Fetch all users from the database
            sample_data = self.database_manager.fetch_all("SELECT * FROM Users")

            # Set the number of rows and columns
            self.ui.showAllUsersTable.setRowCount(len(sample_data))
            if len(sample_data) > 0:
                self.ui.showAllUsersTable.setColumnCount(len(sample_data[0]))
            else:
                self.ui.showAllUsersTable.setColumnCount(0)

            # Insert data into the table
            for row_idx, row_data in enumerate(sample_data):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.ui.showAllUsersTable.setItem(row_idx, col_idx, item)

        except Exception as e:
            print(f"An error occurred while populating the table: {str(e)}")
            show_error_message(self, f"An error occurred while populating the table: {str(e)}")


    def add_user(self):
        try:
            username = self.ui.userNameInput.text()
            password = self.ui.userPasswordInput.text()
            email = self.ui.userEmailInput.text()
            user_role = self.ui.userRoleInput.currentText()

            success = self.database_manager.register_user(username, password, email, user_role)

            if success:
                show_error_message(self, "User added successfully")
                self.populate_table_with_sample_data()
            else:
                show_error_message(self, "Error: Failed to register user.")
        except Exception as e:
            print(f"An error occurred during user registration: {str(e)}")
            show_error_message(self, f"An error occurred during user registration: {str(e)}")


        
    
    def open_login_page(self):
        self.login_form = LoginPageUI()
        self.hide()
        time.sleep(0.2)
        self.login_form.show()

    def open_signup_page(self):
        self.signup_form = SignUpPageUI()
        self.hide()
        time.sleep(0.2)
        self.signup_form.show()  

def main():

    try:
        app = QApplication(sys.argv)
        # window = LoginPageUI(DatabaseManager("hotel_management.db"))
        window=MainUIClass(DatabaseManager("hotel_management.db"))
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
