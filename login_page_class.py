from PyQt5.QtWidgets import  QMainWindow
from loginPage import Ui_MainWindow as logi
import time
# from admin_landing_page import Ui_MainWindow as admin
# from Customer_class import CustomerLandingPage
from show_messages import show_error_message, show_success_message
# from signup_class import SignUpPageUI
from manager_class import MainUIClass
from front_desk_class import FrontDeskLandingPage

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
            selected_user_role=self.ui.signInRole.currentText()
            
            if (str(user_role).lower() == "manager" and selected_user_role.lower() =="manager") :
                self.open_manager_landing_page()
            elif (str(user_role).lower() == "front desk" and selected_user_role.lower() =="front desk") :
                self.open_front_desk_landing_page()
            elif (str(user_role).lower() == "guest" and selected_user_role.lower() =="guest") :
                self.open_customer_landing_page()
            else:
                show_error_message(self, "User Not Found")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            show_error_message(self, f"An error occurred: {str(e)}")


    def open_manager_landing_page(self):
        self.landing_form=MainUIClass(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.landing_form.show()

    def open_front_desk_landing_page(self):
        
        self.landing_form=FrontDeskLandingPage(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.landing_form.show()

    def open_customer_landing_page(self):
        self.landing_form = CustomerLandingPage(self.database_manager)
        self.hide()
        time.sleep(0.2)
        self.landing_form.show()
