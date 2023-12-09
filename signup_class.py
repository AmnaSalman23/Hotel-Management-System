from PyQt5.QtWidgets import  QMainWindow
from SignUpForm import Ui_MainWindow as sign
import time
import re
from front_desk import Ui_MainWindow as front
# from Customer_class import CustomerLandingPage
from show_messages import show_error_message, show_success_message
# from login_page_class import LoginPageUI
# from front_desk_class import FrontDeskLandingPage
from manager_class import MainUIClass

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