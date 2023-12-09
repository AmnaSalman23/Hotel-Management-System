
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from ManagerLandingPage import Ui_MainWindow  # Import the generated UI class
from PyQt5.QtWidgets import QMainWindow, QLabel
import time
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from show_messages import show_error_message, show_success_message
# from login_page_class import LoginPageUI
LoggedUserName=""
LoggedUserType=""
LoggedUserPassword=""

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
        self.ui.profilePageBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.userProfile))
        self.ui.backupDatabaseNavigate.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.manageDatabaseBackupPage))
        self.ui.backupDatabaseBtn.clicked.connect(self.backup_database)
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
        
        global LoggedUserName
        userName=LoggedUserName
        global LoggedUserPassword
        password=LoggedUserPassword
        self.ui.userProfileName.setText(userName)
        self.ui.userProfilePassword.setText(password)
        self.ui.logoutBtn.clicked.connect(self.open_login_page)
        self.sidebar_visible = False

    def edit_username_and_password(self):
        username = self.ui.userProfileName.text()
        password = self.ui.userProfilePassword.text()
        # if not self.is_valid_name(username):
        #     show_error_message(self, "Error: Invalid username.")
        #     return

        # if not self.is_valid_password(password):
        #     show_error_message(self, "Error: Invalid password.")
        #     return
        query = "UPDATE Users SET Username=?, Password=? WHERE Username=?"
        global LoggedUserName
        global LoggedUserPassword
        self.database_manager.execute_query(query, (username, password, LoggedUserName))
        LoggedUserName=username
        LoggedUserPassword=password
        self.ui.userProfileName.setText(username)
        self.ui.userProfilePassword.setText(password)
        show_success_message(self, "User details updated successfully")
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
            show_error_message(self, f"An error occurred while saving the edited row: {str(e)}")

    def add_user(self):
        try:
            username = self.ui.userNameInput.text()
            password = self.ui.userPasswordInput.text()
            email = self.ui.userEmail.text()
            # user_role = self.ui.userRoleInput.currentText()
            user_role = self.ui.comboBox_6.currentText()

            success = self.database_manager.register_user(username, password, email, user_role)

            if success:
                show_success_message(self, "User added successfully")
                self.populate_table_with_sample_data()
            else:
                show_error_message(self, "Error: Failed to register user.")
        except Exception as e:
            print(f"An error occurred during user registration: {str(e)}")
            show_error_message(self, f"An error occurred during user registration: {str(e)}")

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

        self.ui.dashboardBtn.setText("Dashboard" if self.sidebar_visible else "")
        self.ui.manageUsersBtn.setText("Manage Staff" if self.sidebar_visible else "")

        self.ui.backupDatabaseNavigate.setText("Backup" if self.sidebar_visible else "")
        self.ui.label.setText("InnSync" if self.sidebar_visible else "Inn\nSync")
        self.ui.profilePageBtn.setText("Profile" if self.sidebar_visible else "")
        self.ui.logoutBtn.setText("Logut" if self.sidebar_visible else "")
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
            show_success_message(self,"Backup canceled by user.")
            return
        # Create the backup directory if it doesn't exist
        if not os.path.exists(backup_directory):
            os.makedirs(backup_directory)
        # Construct the backup file path (e.g., backup/hotel_management_backup.db)
        backup_file_path = os.path.join(backup_directory, 'hotel_management_backup.db')
        try:
            # Copy the original database file to the backup location
            shutil.copy(original_db_path, backup_file_path)
            show_success_message(self,f"Backup created successfully at: {backup_file_path}")
        except Exception as e:
            show_success_message(self,f"Error creating backup: {e}")
# Call the function to create a backup