import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
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
import re



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
    def add_service(self, service_name, description, price):
        query = "INSERT INTO Services (ServiceName, Description, Price) VALUES (?, ?, ?)"
        self.execute_query(query, (service_name, description, price))

    def insert_booking(self, customer_id, room_number, check_in_datetime, check_out_datetime, is_assured):
        try:
            connection = sqlite3.connect("hotel_management.db")
            cursor = connection.cursor()

            cursor.execute('''
                INSERT INTO RoomBookings (CustomerID, RoomNumber, CheckInDateTime, CheckOutDateTime, IsAssured)
                VALUES (?, ?, ?, ?, ?)
            ''', (customer_id, room_number, check_in_datetime, check_out_datetime, is_assured))

            connection.commit()
            connection.close()

            # Provide feedback to the user with the correct parent widget
            # QMessageBox.information(parent_widget, "Booking Successful", "Room booked successfully!")

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
             

    def cancel_booking_by_id(self, booking_id):
        try:
            connection = sqlite3.connect("hotel_management.db")
            cursor = connection.cursor()

            cursor.execute('''
                DELETE FROM RoomBookings
                WHERE BookingID = ?
            ''', (booking_id,))

            connection.commit()
            connection.close()

            # Provide feedback to the user (you can customize this message)
            QMessageBox.information(self, "Booking Canceled", "Booking canceled successfully!")

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            # Handle the error (you can customize this part)




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
        self.ui.registerNowBtn.clicked.connect(self.open_signup_page)
        

 


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
        self.signup_form = SignUpPageUI(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.signup_form.show()

    # def logn_successful(self):
    #     if self.ui.lineEdit.text() == "admin" and self.ui.lineEdit_2.text() == "admin":
    #         self.open_landing_page()
    #     # self.open_landing_page

    def open_landing_page(self):
        self.landing_form = MainUIClass(self.database_manager)
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
        self.landing_form = AdminLandingPage(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.landing_form.show()

    def open_manager_landing_page(self):
        self.landing_form=MainUIClass(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.landing_form.show()

    def open_staff_landing_page(self):
        # Open the staff landing page
        pass

    def open_customer_landing_page(self):
        self.landing_form = CustomerLandingPage(self.database_manager)
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

        # Validate email, name, and password
        if not self.is_valid_email(email):
            show_error_message(self, "Error: Invalid email address.")
            return

        if not self.is_valid_name(username):
            show_error_message(self, "Error: Invalid username.")
            return

        if not self.is_valid_password(password):
            show_error_message(self, "Error: Invalid password.")
            return

        if password != confirm_password:
            show_error_message(self, "Error: Passwords do not match.")
            return

        # Check if the user with the same username or email already exists
        if not self.database_manager.user_exists(username, email):
            # Register the user
            if self.database_manager.register_user(username, password, email, user_role):
                self.signup_successful()
            else:
                show_error_message(self, "Error: Failed to register user.")
        else:
            show_error_message(self, "Error: User with the same username or email already exists.")

    def is_valid_email(self, email):
        # Simple email validation using a regular expression
        pattern = r'^\S+@\S+\.\S+$'
        return re.match(pattern, email) is not None

    def is_valid_name(self, name):
        # Simple name validation - you can customize this based on your requirements
        return len(name) > 0

    def is_valid_password(self, password):
        # Simple password validation - you can customize this based on your requirements
        return len(password) >= 8

    def signup_successful(self):
        customer= CustomerLandingPage(DatabaseManager("hotel_management.db"))
        self.hide()
        customer.show()  # Pass the database_manager to LoginPageUI

    

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
        self.login_form = LoginPageUI(self.database_manager)
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
        self.ui.serviceName.setPlaceholderText("Service Name")
        self.ui.servicePrice.setPlaceholderText("Price")
        self.ui.serviceDescription.setPlaceholderText("Description")
        self.populate_table_with_sample_data()
        self.ui.showAllUsers.itemSelectionChanged.connect(self.show_selected_message)
        self.ui.deleteUserBtn.clicked.connect(self.delete_selected_row)
        self.ui.updateUserBtn.clicked.connect(self.edit_selected_row)
        self.ui.userProfileName.setPlaceholderText("Name")
        self.ui.userProfilePassword.setPlaceholderText("Password")
        global LoggedUserName
        global LoggedUserPassword
        self.ui.userProfileName.setText(LoggedUserName)
        self.ui.userProfilePassword.setText(LoggedUserPassword)
        self.ui.addServiceBtn.clicked.connect(self.add_service_to_database)
        self.populate_table_with_services()
        self.ui.showAllServices.itemSelectionChanged.connect(self.show_selected_message_2)
        self.ui.deleteServiceBtn.clicked.connect(self.delete_selected_row_2)
        self.ui.updateServiceBtn.clicked.connect(self.edit_selected_row_2)
        self.ui.logoutBtn.clicked.connect(self.open_login_page)

    



        # self.ui.deleteServiceBtn.setText("")


        # Initialize sidebar state (visible)
        self.sidebar_visible = False
    def open_login_page(self):
        self.login_form = LoginPageUI(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.login_form.show()
    def show_selected_message_2(self):
        selected_items = self.ui.showAllServices.selectedItems()
        if selected_items:
            selected_message = "Selected: "
            selected_row_data = []
            for item in selected_items:
                selected_message += f"{item.text()} "
                selected_row_data.append(item.text())
            print(selected_message)
            self.selected_row_data = selected_row_data
    def edit_selected_row_2(self):
        if hasattr(self, 'selected_row_data') and self.selected_row_data:
            # Create a dialog for editing data
            dialog = QDialog(self)
            dialog.setWindowTitle("Edit Row")

            layout = QVBoxLayout()

            # Add input fields for editing
            labels = ["Name:", "Price:", "Description:"]
            line_edits = [QLineEdit(data) for data in self.selected_row_data[1:]]
            for label, line_edit in zip(labels, line_edits):
                row_layout = QVBoxLayout()
                row_layout.addWidget(QLabel(label))
                row_layout.addWidget(line_edit)
                layout.addLayout(row_layout)
            save_button = QPushButton("Save")
            cancel_button = QPushButton("Cancel")
            layout.addWidget(save_button)
            layout.addWidget(cancel_button)

            dialog.setLayout(layout)

            # Connect signals
            save_button.clicked.connect(lambda: self.save_edited_row(dialog, line_edits))
            cancel_button.clicked.connect(dialog.reject)

            dialog.exec_()
    def save_edited_row_2(self, dialog, line_edits):
        try:
            # Extract edited data
            edited_data = [line_edit.text() for line_edit in line_edits]

            # Update the database
            query = "UPDATE Services SET Name=?, Price=?, Description=?"
            self.database_manager.execute_query(query, (*edited_data, self.selected_row_data[0]))

            # Update the table
            selected_row = self.ui.showAllServices.currentRow()
            for col_idx, col_data in enumerate(edited_data):
                item = QTableWidgetItem(col_data)
                self.ui.showAllServices.setItem(selected_row, col_idx + 1, item)  # Adjust column index

            print(f"Row {self.selected_row_data} edited successfully.")
            dialog.accept()
        except Exception as e:
            print(f"An error occurred while saving the edited row: {str(e)}")
            show_error_message(self, f"An error occurred while saving the edited row: {str(e)}")

    def add_service_to_database(self):
        service_name = self.ui.serviceName.text()
        description = self.ui.serviceDescription.toPlainText()
        price = float(self.ui.servicePrice.text())  # Assuming price is a float

        try:
            # Add service to the database
            self.database_manager.add_service(service_name, description, price)
            show_error_message(self, "Service added successfully")

            # Refresh the table to show all services
            self.populate_table_with_services()

            # Optionally, clear input fields
            self.ui.serviceName.clear()
            self.ui.serviceDescription.clear()
            self.ui.servicePrice.clear()
        except Exception as e:
            show_error_message(self, f"Error adding service: {str(e)}")

    def populate_table_with_services(self):
        try:
            # Fetch all services from the database
            services_data = self.database_manager.fetch_all("SELECT * FROM Services")

            # Set the number of rows and columns
            self.ui.showAllServices.setRowCount(len(services_data))
            if len(services_data) > 0:
                self.ui.showAllServices.setColumnCount(len(services_data[0]))
            else:
                self.ui.showAllServices.setColumnCount(0)

            # Insert data into the table
            for row_idx, row_data in enumerate(services_data):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.ui.showAllServices.setItem(row_idx, col_idx, item)

        except Exception as e:
            show_error_message(self, f"An error occurred while populating the services table: {str(e)}")


    def show_selected_message(self):
        selected_items = self.ui.showAllUsers.selectedItems()
        if selected_items:
            selected_message = "Selected: "
            selected_row_data = []
            for item in selected_items:
                selected_message += f"{item.text()} "
                selected_row_data.append(item.text())
            print(selected_message)
            self.selected_row_data = selected_row_data  # Store selected row data for deletion
    def delete_selected_row_2(self):
        if hasattr(self, 'selected_row_data') and self.selected_row_data:
            reply = QMessageBox.question(
                self,
                'Delete Row',
                f'Do you want to delete the selected row {self.selected_row_data}?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                try:
                    # Delete the row from the database
                    query = "DELETE FROM Services WHERE ServiceName = ? AND Price = ?"
                    self.database_manager.execute_query(query, (self.selected_row_data[0], self.selected_row_data[2]))

                    # Delete the row from the table
                    selected_row = self.ui.showAllServices.currentRow()
                    self.ui.showAllServices.removeRow(selected_row)

                    print(f"Row {self.selected_row_data} deleted successfully.")
                except Exception as e:
                    print(f"An error occurred while deleting the row: {str(e)}")
                    show_error_message(self, f"An error occurred while deleting the row: {str(e)}")
    def delete_selected_row(self):
        if hasattr(self, 'selected_row_data') and self.selected_row_data:
            reply = QMessageBox.question(
                self,
                'Delete Row',
                f'Do you want to delete the selected row {self.selected_row_data}?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                try:
                    # Delete the row from the database
                    query = "DELETE FROM Users WHERE Username = ? AND Password = ?"
                    self.database_manager.execute_query(query, (self.selected_row_data[0], self.selected_row_data[1]))

                    # Delete the row from the table
                    selected_row = self.ui.showAllUsers.currentRow()
                    self.ui.showAllUsers.removeRow(selected_row)

                    print(f"Row {self.selected_row_data} deleted successfully.")
                except Exception as e:
                    print(f"An error occurred while deleting the row: {str(e)}")
                    show_error_message(self, f"An error occurred while deleting the row: {str(e)}")

    def edit_selected_row(self):
        if hasattr(self, 'selected_row_data') and self.selected_row_data:
            # Create a dialog for editing data
            dialog = QDialog(self)
            dialog.setWindowTitle("Edit Row")

            layout = QVBoxLayout()

            # Add input fields for editing
            labels = ["Username:", "Password:", "Email:", "User Type:"]
            line_edits = [QLineEdit(data) for data in self.selected_row_data[1:]]  # Exclude UserID

            for label, line_edit in zip(labels, line_edits):
                row_layout = QVBoxLayout()
                row_layout.addWidget(QLabel(label))
                row_layout.addWidget(line_edit)
                layout.addLayout(row_layout)

            # Add save and cancel buttons
            save_button = QPushButton("Save")
            cancel_button = QPushButton("Cancel")
            layout.addWidget(save_button)
            layout.addWidget(cancel_button)

            dialog.setLayout(layout)

            # Connect signals
            save_button.clicked.connect(lambda: self.save_edited_row(dialog, line_edits))
            cancel_button.clicked.connect(dialog.reject)

            dialog.exec_()

    def save_edited_row(self, dialog, line_edits):
        try:
            # Extract edited data
            edited_data = [line_edit.text() for line_edit in line_edits]

            # Update the database
            query = "UPDATE Users SET Username=?, Password=?, Email=?, UserType=? WHERE UserID=?"
            self.database_manager.execute_query(query, (*edited_data, self.selected_row_data[0]))

            # Update the table
            selected_row = self.ui.showAllUsers.currentRow()
            for col_idx, col_data in enumerate(edited_data):
                item = QTableWidgetItem(col_data)
                self.ui.showAllUsers.setItem(selected_row, col_idx + 1, item)  # Adjust column index

            print(f"Row {self.selected_row_data} edited successfully.")
            dialog.accept()
        except Exception as e:
            print(f"An error occurred while saving the edited row: {str(e)}")
            show_error_message(self, f"An error occurred while saving the edited row: {str(e)}")


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
    def __init__(self, database_manager):
        super().__init__()
        self.database_manager = database_manager
        # Create an instance of the generated UI class
        self.ui = cust()
        self.ui.setupUi(self)

        # elf.ui.pushButton_2.clicked.connect(self.open_login_page)
        # self.ui.pushButton_4.clicked.connect(self.open_signup_page)s

        self.ui.dashboardBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Dashboard))
        self.ui.bookRoomBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.bookRoomPage))
        # self.ui.manageBookingBtn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.manageBookingPage))
        self.ui.profilePageBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.userProfile))
        # self.ui.managePaymentsBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.managePaymentsPage))
        self.ui.navBar.clicked.connect(self.toggle_sidebar)
        self.ui.bookRoomBtn.clicked.connect(self.book_room)
        self.ui.cancelBookingBtn.clicked.connect(self.cancel_booking)
        self.ui.logoutBtn.clicked.connect(self.open_login_page)

    def book_room(self):
        # You need to implement the logic for booking a room here
        # This might involve collecting necessary information from the user
        # and then inserting a new record into the RoomBookings table

        # For example:
        customer_id = 1  # Replace with the actual customer ID
        room_number = 101  # Replace with the actual room number
        check_in_datetime = "2023-01-01 12:00:00"  # Replace with the actual check-in datetime
        check_out_datetime = "2023-01-03 12:00:00"  # Replace with the actual check-out datetime
        is_assured = True  # Replace with the actual assurance status

        # Insert the booking into the RoomBookings table
        self.database_manager.insert_booking(customer_id, room_number, check_in_datetime, check_out_datetime, is_assured)
        show_error_message(self, "Room booked successfully!")

    def cancel_booking(self):
        # You need to implement the logic for canceling a booking here
        # This might involve selecting a booking from the RoomBookings table
        # and then deleting the corresponding record

        # For example:
        booking_id_to_cancel = 1  # Replace with the actual booking ID to cancel

        # Cancel the booking
        self.database_manager.cancel_booking_by_id(booking_id_to_cancel)
        


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
        self.ui.showAllUsersTable.itemSelectionChanged.connect(self.show_selected_message)
        self.ui.deleteUserBtn.clicked.connect(self.delete_selected_row)
        self.ui.updateUserBtn.clicked.connect(self.edit_selected_row)
        
        

        self.ui.userProfileName=LoggedUserName
        self.ui.userProfilePassword=LoggedUserPassword

        # Add sample data to the table
        self.populate_table_with_sample_data()
        self.ui.logoutBtn.clicked.connect(self.open_login_page)
        
    def show_selected_message(self):
        selected_items = self.ui.showAllUsersTable.selectedItems()
        if selected_items:
            selected_message = "Selected: "
            selected_row_data = []
            for item in selected_items:
                selected_message += f"{item.text()} "
                selected_row_data.append(item.text())
            print(selected_message)
            self.selected_row_data = selected_row_data  # Store selected row data for deletion
            
    def edit_selected_row(self):
        if hasattr(self, 'selected_row_data') and self.selected_row_data:
            # Create a dialog for editing data
            dialog = QDialog(self)
            dialog.setWindowTitle("Edit Row")

            layout = QVBoxLayout()

            # Add input fields for editing
            labels = ["Username:", "Password:", "Email:", "User Type:"]
            line_edits = [QLineEdit(data) for data in self.selected_row_data[1:]]
            for label, line_edit in zip(labels, line_edits):
                row_layout = QVBoxLayout()
                row_layout.addWidget(QLabel(label))
                row_layout.addWidget(line_edit)
                layout.addLayout(row_layout)

            save_button = QPushButton("Save")
            cancel_button = QPushButton("Cancel")
            layout.addWidget(save_button)
            layout.addWidget(cancel_button)

            dialog.setLayout(layout)

            # Connect signals
            save_button.clicked.connect(lambda: self.save_edited_row(dialog, line_edits))
            cancel_button.clicked.connect(dialog.reject)

            dialog.exec_()

    
    def save_edited_row(self, dialog, line_edits):
        try:
            # Extract edited data
            edited_data = [line_edit.text() for line_edit in line_edits]

            # Update the database
            query = "UPDATE Users SET Username=?, Password=?, Email=?, UserType=? WHERE UserID=?"
            self.database_manager.execute_query(query, (*edited_data, self.selected_row_data[0]))

            # Update the table
            selected_row = self.ui.showAllUsersTable.currentRow()
            for col_idx, col_data in enumerate(edited_data):
                item = QTableWidgetItem(col_data)
                self.ui.showAllUsersTable.setItem(selected_row, col_idx + 1, item)  # Adjust column index

            print(f"Row {self.selected_row_data} edited successfully.")
            dialog.accept()
        except Exception as e:
            print(f"An error occurred while saving the edited row: {str(e)}")
            show_error_message(self, f"An error occurred while saving the edited row: {str(e)}")
        
    def delete_selected_row(self):
        if hasattr(self, 'selected_row_data') and self.selected_row_data:
            reply = QMessageBox.question(
                self,
                'Delete Row',
                f'Do you want to delete the selected row {self.selected_row_data}?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                try:
                    # Delete the row from the database
                    query = "DELETE FROM Users WHERE Username = ? AND Password = ?"
                    self.database_manager.execute_query(query, (self.selected_row_data[0], self.selected_row_data[1]))

                    # Delete the row from the table
                    selected_row = self.ui.showAllUsersTable.currentRow()
                    self.ui.showAllUsersTable.removeRow(selected_row)

                    print(f"Row {self.selected_row_data} deleted successfully.")
                except Exception as e:
                    print(f"An error occurred while deleting the row: {str(e)}")
                    show_error_message(self, f"An error occurred while deleting the row: {str(e)}")
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
        self.login_form = LoginPageUI(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.login_form.show()

    def open_signup_page(self):
        self.signup_form = SignUpPageUI(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.signup_form.show()  

def main():

    try:
        app = QApplication(sys.argv)
        # window = LoginPageUI(DatabaseManager("hotel_management.db"))
        window=LoginPageUI(DatabaseManager("hotel_management.db"))
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
