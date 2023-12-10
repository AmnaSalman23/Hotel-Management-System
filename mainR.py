import sys
import re
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QIcon

from database_manager import DatabaseManager
from loginPage import Ui_MainWindow as logi
from show_messages import show_error_message, show_success_message

from front_desk import Ui_MainWindow as front
from customer_landing_page import Ui_MainWindow as cust
from utils import Utils
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QMainWindow, QLabel
import matplotlib.pyplot as plt
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from loginPage import Ui_MainWindow as logi
from ManagerLandingPage import Ui_MainWindow as Ui_MainWindow
from SignUpForm import Ui_MainWindow as sign
# Add any additional imports as needed...






LoggedUserName=""
LoggedUserPassword=""

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
            selected_user_role=self.ui.signInRole.currentText()
            
            if (str(user_role).lower() == "manager" and selected_user_role.lower() =="manager") :
                self.open_manager_landing_page()
            elif (str(user_role).lower() == "front desk" and selected_user_role.lower() =="front desk") :
                self.open_front_desk_landing_page(self.database_manager)
            elif (str(user_role).lower() == "guest" and selected_user_role.lower() =="guest") :
                self.open_customer_landing_page()
            else:
                show_error_message( "User Not Found")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            show_error_message(f"An error occurred: {str(e)}")
    def open_front_desk_landing_page(self, database_manager):
        self.landing_form=FrontDeskLandingPage(database_manager)
        self.hide()
        time.sleep(0.2)
        self.landing_form.show()

    def open_manager_landing_page(self):
        self.landing_form=MainUIClass(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.landing_form.show()

    # def open_front_desk_landing_page(self):
        
    #     self.landing_form=FrontDeskLandingPage(self.database_manager)
    #     self.hide()
    #     time.sleep(0.2)
    #     self.landing_form.show()

    def open_customer_landing_page(self):
        self.landing_form = CustomerLandingPage(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.landing_form.show()





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
        self.ui.addGuestBtn.clicked.connect(self.add_guest)
        self.get_all_rooms()
        self.ui.deleteUserBtn.clicked.connect(self.delete_guest)
        self.get_all_room_types()
        global LoggedUserName
        self.ui.userProfileName.setText(LoggedUserName)
        global LoggedUserPassword
        self.ui.userProfilePassword.setText(LoggedUserPassword)
        self.ui.addReservationBtn.clicked.connect(self.add_reservation)
        self.get_all_users()
        self.get_all_rooms()


    def get_all_users(self):
        users = self.database_manager.fetch_all('''SELECT * FROM Users''')
        self.ui.label_24.setText(str(len(users)))
        # return users
    
    # def show_all_guests(self):

    def add_reservation(self):
        # For example:
        guest_name = self.ui.customerNameInput.text()
        room_number = self.ui.roomInput.currentText()
        check_in_date = self.ui.checkInDate.text()
        check_out_date = self.ui.checkOutDate.text()
        # Insert the guest into the Guests table
        self.database_manager.add_reservation(guest_name, room_number, check_in_date, check_out_date)
        show_success_message("Reservation added successfully")
        self.show_all_guests()
        
    def get_all_rooms(self):
        rooms = self.database_manager.fetch_all('''
            SELECT
                Rooms.room_number
            FROM Rooms
            Where Rooms.availability_status = "Available"
        ''')
        self.ui.label_27.setText(str(len(rooms)))
        # return rooms
    
    def get_all_room_types(self):
        room_types = self.database_manager.fetch_all('''
            SELECT
                Rooms.room_type
            FROM Rooms
        ''')
        self.ui.roomInput_2.addItems([str(room_type[0]) for room_type in room_types])
        return room_types
    def delete_guest(self):
        # For example:
        guest_id = self.ui.showAllUsersTable.item(self.ui.showAllUsersTable.currentRow(), 0).text()
        # Insert the guest into the Guests table
        self.database_manager.delete_guest(guest_id)
        show_success_message("Guest deleted successfully")
        self.show_all_guests()
        
    def add_guest(self):
        # For example:
        first_name = self.ui.guestFirstNameInput.text()
        last_name = self.ui.guestLastName.text()
        email = self.ui.guestEmail.text()
        phone_number = self.ui.guestPhoneNumber.text()
        address = self.ui.guestAdress.text()
        room_number = self.ui.roomInput.currentText()
        check_in_date = self.ui.checkInDate.text()
        country = self.ui.countryInput.currentText()
        room_type = self.ui.roomInput_2.currentText()
        checkoutdate=self.ui.checkOutDate.text()
        # Insert the guest into the Guests table
        self.database_manager.add_guest_with_room(first_name, last_name, email, phone_number, address, country, check_in_date, checkoutdate, room_number, room_type)
        show_success_message("Guest added successfully")
        self.show_all_guests()
        
    def open_login_page(self):
        Utils.open_login_page(self.database_manager)
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
        

    def show_all_guests(self):
        # Assuming self.database_manager.fetch_all() returns a list of tuples
        sample_data = self.database_manager.fetch_all('''
            SELECT
                Guests.guest_id,
                Guests.first_name,
                Guests.last_name,
                Guests.email,
                Guests.phone_number,
                Guests.address,
                Guests.nationality,
                Guests.check_in_date,
                Guests.check_out_date,
                Rooms.room_number,
                Rooms.room_type
            FROM Guests
            LEFT JOIN Reservations ON Guests.guest_id = Reservations.guest_id
            LEFT JOIN Rooms ON Reservations.room_id = Rooms.room_id
        ''')

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

class MainUIClass(QMainWindow):
    def __init__(self, database_manager):
        super().__init__()
        self.database_manager = database_manager
        # Create an instance of the generated UI class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.dashboardBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Dashboard))
        self.ui.manageRoomBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.manageRoomsPage))
        # PAGE 2 Settings Page
        self.ui.manageUsersBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.manageStaffPage))
        self.ui.profilePageBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.userProfile))
        self.ui.backupDatabaseNavigate.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.manageDatabaseBackupPage))
        # self.ui.backupDatabaseBtn.clicked.connect(self.backup_database)
        self.ui.addUserBtn.clicked.connect(self.add_user)
        self.ui.navBar.clicked.connect(self.toggle_sidebar)
        self.ui.updateProfileBtn.clicked.connect(self.edit_username_and_password)
        self.loadAllEmployeesGraph()
        self.ui.userNameInput.setPlaceholderText("Name")
        self.ui.userEmail.setPlaceholderText("Email")
        self.ui.userPasswordInput.setPlaceholderText("Password")
        self.populate_table_with_sample_data()
        self.ui.showAllUsers.itemSelectionChanged.connect(self.show_selected_message)
        self.ui.deleteUserBtn.clicked.connect(self.delete_selected_row)
        self.ui.updateUserBtn.clicked.connect(self.edit_selected_row)
        self.ui.userProfileName.setPlaceholderText("Name")
        self.ui.userProfilePassword.setPlaceholderText("Password")
        self.ui.totla_users_label.setText(str(self.all_users()))
        self.ui.roomNoInput.setPlaceholderText("Room Number")
        self.ui.roomTypeInput.setPlaceholderText("Room Type")
        self.ui.occupancyLimitInput.setPlaceholderText("Occupancy Limit")
        self.set_available_no_of_rooms()
        self.ui.addRoomBtn.clicked.connect(self.add_room)
        self.ui.deleteRoomBtn.clicked.connect(self.delete_selected_room)
    
        
        global LoggedUserName
        userName=LoggedUserName
        global LoggedUserPassword
        password=LoggedUserPassword
        self.ui.userProfileName.setText(userName)
        self.ui.userProfilePassword.setText(password)
        self.ui.logoutBtn.clicked.connect(self.open_login_page)
        self.sidebar_visible = False
        self.show_all_rooms_in_table()

    def show_all_rooms_in_table(self):
        # Assuming self.database_manager.fetch_all() returns a list of tuples
        sample_data = self.database_manager.fetch_all('''
            SELECT
                Rooms.room_id,
                Rooms.room_number,
                Rooms.room_type,
                Rooms.occupancy_limit,
                Rooms.availability_status
            FROM Rooms
        ''')

        # Clear existing data in the table
        self.ui.allRoomsTable.setRowCount(0)

        if len(sample_data) > 0:
            # Set the number of rows and columns in the table
            self.ui.allRoomsTable.setRowCount(len(sample_data))
            self.ui.allRoomsTable.setColumnCount(len(sample_data[0]))

            # Populate the table with data
            for row_num, row_data in enumerate(sample_data):
                for col_num, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.ui.allRoomsTable.setItem(row_num, col_num, item)

        else:
            # If there is no data, set columns to 0
            self.ui.showAllRoomsTable.setColumnCount(0)

    def delete_selected_room(self):
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
                    query = "DELETE FROM Rooms WHERE RoomNumber = ? AND RoomType = ?"
                    self.database_manager.execute_query(query, (self.selected_row_data[0], self.selected_row_data[1]))
                    print(f"Row {self.selected_row_data} deleted successfully.")
                except Exception as e:
                    print(f"An error occurred while deleting the row: {str(e)}")
                    show_error_message(f"An error occurred while deleting the row: {str(e)}")

    def add_room(self):
        room_number = self.ui.roomNoInput.text()
        room_type = self.ui.roomTypeInput.currentText()
        occupancy_limit = self.ui.occupancyLimitInput.currentText()
        # Insert the guest into the Guests table
        self.database_manager.add_room(room_number, room_type, occupancy_limit,"Available")
        show_success_message("Room added successfully")
        self.set_available_no_of_rooms()
        # self.get_all_rooms()
        # self.get_all_room_types()
        # self.ui.roomNoInput.setText("")
        # self.ui.roomTypeInput.setText("")
        # self.ui.occupancyLimitInput.setText("")


    def set_available_no_of_rooms(self):
        available_rooms = self.database_manager.fetch_all('''
            SELECT
                COUNT(Rooms.room_id)
            FROM Rooms
            Where Rooms.availability_status = "Available"
        ''')
        self.ui.label_13.setText(str(available_rooms[0][0]))
    def edit_username_and_password(self):
        username = self.ui.userProfileName.text()
        password = self.ui.userProfilePassword.text()
        
        query = "UPDATE Users SET Username=?, Password=? WHERE Username=?"
        global LoggedUserName
        global LoggedUserPassword
        self.database_manager.execute_query(query, (username, password, LoggedUserName))
        LoggedUserName=username
        LoggedUserPassword=password
        self.ui.userProfileName.setText(username)
        self.ui.userProfilePassword.setText(password)
        show_success_message("User details updated successfully")
        # self.open_login_page()

    def open_login_page(self):
        self.login_form = LoginPageUI(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.login_form.show()
    
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
                    print(f"Row {self.selected_row_data} deleted successfully.")
                except Exception as e:
                    print(f"An error occurred while deleting the row: {str(e)}")
                    show_error_message(f"An error occurred while deleting the row: {str(e)}")
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
                    show_error_message(f"An error occurred while deleting the row: {str(e)}")

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
            query = "UPDATE Users SET Username=?, Password=?, Email=?, Role=? WHERE user_id=?"
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
            show_error_message(f"An error occurred while saving the edited row: {str(e)}")

    def add_user(self):
        try:
            username = self.ui.userNameInput.text()
            password = self.ui.userPasswordInput.text()
            email = self.ui.userEmail.text()
            # user_role = self.ui.userRoleInput.currentText()
            user_role = self.ui.comboBox_6.currentText()

            success = self.database_manager.register_user(username, password, email, user_role)

            if success:
                show_success_message("User added successfully")
                self.populate_table_with_sample_data()
            else:
                show_error_message("Error: Failed to register user.")
        except Exception as e:
            print(f"An error occurred during user registration: {str(e)}")
            show_error_message(f"An error occurred during user registration: {str(e)}")

    def all_users(self):
        sample_data = self.database_manager.fetch_all("SELECT * FROM Users")
        return len(sample_data)
    
    def populate_table_with_sample_data(self):
        try:
            # Fetch all users from the database
            sample_data = self.database_manager.fetch_all("SELECT * FROM Users")

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
            show_error_message(f"An error occurred while populating the table: {str(e)}")
    
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

        self.ui.dashboardBtn.setText("Dashboard" if self.sidebar_visible else "")
        self.ui.manageUsersBtn.setText("Staff" if self.sidebar_visible else "")
        self.ui.manageRoomBtn.setText("Rooms" if self.sidebar_visible else "")
        self.ui.backupDatabaseNavigate.setText("Backup" if self.sidebar_visible else "")
        self.ui.label.setText("InnSync" if self.sidebar_visible else "Inn\nSync")
        self.ui.profilePageBtn.setText("Profile" if self.sidebar_visible else "")
        self.ui.logoutBtn.setText("   Logut" if self.sidebar_visible else "")
        self.ui.navBar.setIcon(QIcon(QPixmap("images/icons8-close-128.png").scaled(60,60)) if self.sidebar_visible else QIcon("images/icons8-hamburger-100.png"))
        if self.sidebar_visible:
            time.sleep(0.2)
            self.ui.frame.setFixedWidth(250)
        else:
            time.sleep(0.2)
            self.ui.frame.setFixedWidth(100)


def backup_database(self):
        # Path to the original database file
        original_db_path = 'hotel_management.db'
        # Open a directory dialog to choose the backup directory
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        backup_directory = filedialog.askdirectory(title="Select Backup Directory")
        root.destroy()  # Close the hidden main window
        # Check if the user canceled the directory selection
        if not backup_directory:
            show_success_message("Backup canceled by user.")
            return
        # Create the backup directory if it doesn't exist
        if not os.path.exists(backup_directory):
            os.makedirs(backup_directory)
        # Construct the backup file path (e.g., backup/hotel_management_backup.db)
        backup_file_path = os.path.join(backup_directory, 'hotel_management_backup.db')
        try:
            # Copy the original database file to the backup location
            shutil.copy(original_db_path, backup_file_path)
            show_success_message(f"Backup created successfully at: {backup_file_path}")
        except Exception as e:
            show_success_message(f"Error creating backup: {e}")
# Call the function to create a backup


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
        user_role = self.ui.signUpRole.currentText()

        # Validate email, name, and password
        if not self.is_valid_email(email):
            show_error_message("Error: Invalid email address.")
            return

        if not self.is_valid_name(username):
            show_error_message("Error: Invalid username.")
            return

        if not self.is_valid_password(password):
            show_error_message("Error: Invalid password.")
            return

        if password != confirm_password:
            show_error_message("Error: Passwords do not match.")
            return

        # Check if the user with the same username or email already exists
        if not self.database_manager.user_exists(username, email):
            # Register the user
            if self.database_manager.register_user(username, password, email, user_role):
                self.signup_successful()
            else:
                show_error_message("Error: Failed to register user.")
        else:
            show_error_message("Error: User with the same username or email already exists.")

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

    def show_password(self):
        if self.ui.showPasswordBtn.isChecked():
            self.ui.userPasswordInput.setEchoMode(0)
            self.ui.userPasswordInput_2.setEchoMode(0)
        else:
            self.ui.userPasswordInput.setEchoMode(2)
            self.ui.userPasswordInput_2.setEchoMode(2)
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

    def signup_successful(self):
        # self.open_login_page()
        if self.ui.signUpRole.currentText() == "Manager":
            self.open_managerPage_page()
        if self.ui.signUpRole.currentText() == "Guest":
            self.open_customer_page()
        if self.ui.signUpRole.currentText() == "Front Desk":
            self.open_front_desk_landing_page()


    def open_front_desk_landing_page(self):
        self.landing_form=FrontDeskLandingPage(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.landing_form.show()
        # self.open_landing_page


    def open_managerPage_page(self):
        self.manager_form = MainUIClass(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.manager_form.show()

    def open_front_desk_page(self):
        self.manager_form = MainUIClass(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.manager_form.show()
        
    def open_customer_page(self):
        self.customer_form = CustomerLandingPage(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.customer_form.show()

    def store_signup_data(self):
        username = self.ui.userNameInput.text()
        password = self.ui.userPasswordInput.text()
        confirm_password = self.ui.userPasswordInput_2.text()
        email = self.ui.userEmailInput.text()
        user_role = self.ui.signUpRole.currentText()

        if password == confirm_password:
            self.store_user_data(username, password, email, user_role)
            self.signup_successful()
        else:
            print("Could not sign up")
            show_error_message("Passwords do not match")
        
    

    def store_user_data(self, username, password, email, user_role):
        query = '''
            INSERT INTO Users (Username, Password, Email, Role)
            VALUES (?, ?, ?, ?)
        '''
        self.database_manager.execute_query(query, (username, password, email, user_role))

def main():

    try:
        app = QApplication(sys.argv)
        window=LoginPageUI(DatabaseManager("hotel_management.db"))
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {str(e)}")



class CustomerLandingPage(QMainWindow):
    def __init__(self, database_manager):
        super().__init__()
        self.database_manager = database_manager
        # Create an instance of the generated UI class
        self.ui = cust()
        self.ui.setupUi(self)
        self.sidebar_visible = False


        self.ui.dashboardBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Dashboard))
        self.ui.bookRoomBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.bookRoomPage))
        # self.ui.manageBookingBtn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.manageBookingPage))
        self.ui.profilePageBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.userProfile))
        # self.ui.managePaymentsBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.managePaymentsPage))
        self.ui.navBar.clicked.connect(self.toggle_sidebar)
        self.ui.bookRoomBtn_3.clicked.connect(self.book_room)
        self.ui.cancelBookingBtn.clicked.connect(self.cancel_booking)
        self.ui.logoutBtn.clicked.connect(self.open_login_page)

    def book_room(self):
        # For example:
        customer_id = 1  # Replace with the actual customer ID
        room_number = 101  # Replace with the actual room number
        check_in_datetime = "2023-01-01 12:00:00"  # Replace with the actual check-in datetime
        check_out_datetime = "2023-01-03 12:00:00"  # Replace with the actual check-out datetime
        is_assured = True  # Replace with the actual assurance status
        # Insert the booking into the RoomBookings table
        self.database_manager.insert_booking(customer_id, room_number, check_in_datetime, check_out_datetime, is_assured)
        show_error_message("Room booked successfully!")

    def cancel_booking(self):
        # For example:
        booking_id_to_cancel = 1  # Replace with the actual booking ID to cancel
        # Cancel the booking
        self.database_manager.cancel_booking_by_id(booking_id_to_cancel)
        
    def toggle_sidebar(self):
        # Toggle the sidebar visibility
        self.sidebar_visible = False if self.sidebar_visible else True
        self.animate_sidebar()

    def animate_sidebar(self):
        self.ui.dashboardBtn.setText("Dashboard" if self.sidebar_visible else "")
        self.ui.bookRoomBtn.setText("Book Room" if self.sidebar_visible else "")
        self.ui.profilePageBtn.setText("Profile" if self.sidebar_visible else "")
        self.ui.logoutBtn.setText("Logut" if self.sidebar_visible else "")
        self.ui.label.setText("InnSync" if self.sidebar_visible else "Inn\nSync")        
        self.ui.navBar.setIcon(QIcon(QPixmap("images/icons8-close-128.png").scaled(60,60)) if self.sidebar_visible else QIcon("images/icons8-hamburger-100.png"))
        if self.sidebar_visible:
            time.sleep(0.2)
            self.ui.frame.setFixedWidth(250)
        else:
            time.sleep(0.2)
            self.ui.frame.setFixedWidth(100)

    def open_login_page(self):
        self.login_form = LoginPageUI(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.login_form.show()

    def open_signup_page(self):
        self.signup_form = SignUpPageUI()
        self.hide()
        time.sleep(0.2)
        self.signup_form.show()

if __name__ == "__main__":
    main()
