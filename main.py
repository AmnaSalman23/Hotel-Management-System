import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
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
# from PyQt5.QtWidgets import QPropertyAnimation, QGraphicsOpacityEffect
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QSize
from PyQt5.QtGui import QIcon
from database import create_database



class LoginPageUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create an instance of the generated UI class
        self.ui = logi()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(self.logn_successful)
        self.ui.pushButton_4.clicked.connect(self.open_signup_page)
    
    def open_signup_page(self):
        self.signup_form = SignUpPageUI()
        self.hide()
        time.sleep(0.2)
        self.signup_form.show()

    def logn_successful(self):
        if self.ui.lineEdit.text() == "admin" and self.ui.lineEdit_2.text() == "admin":
            self.open_landing_page()
        # self.open_landing_page

    def open_landing_page(self):
        self.landing_form = MainUIClass()
        self.hide()
        time.sleep(0.2)
        self.landing_form.show()
    
class SignUpPageUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create an instance of the generated UI class
        self.ui = sign()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(self.signup_successful)
        self.ui.pushButton_4.clicked.connect(self.open_login_page)
    
    def open_login_page(self):
        self.login_form = LoginPageUI()
        self.hide()
        time.sleep(0.2)
        self.login_form.show()

    def signup_successful(self):
        self.open_login_page()
        # self.open_landing_page
    
class MainUIClass(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create an instance of the generated UI class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        
        # self.setWindowFlags(Qt.FramelessWindowHint)  # Remove the default title bar
        # self.ui.frame_7.mousePressEvent = self.onTitleBarMousePress
        # self.ui.frame_7.mouseMoveEvent = self.onTitleBarMouseMove
        # self.ui.centralwidget.layout().setContentsMargins(0, 0, 0, 0)

        
        # self.ui.closeBtn.clicked.connect(self.close_application)
        # self.ui.resizeBtn.clicked.connect(self.resize_application)
        # self.ui.minimizeBtn.clicked.connect(self.minimize_application)
        
        self.ui.dashboardBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Dashboard))
        
        # PAGE 2 Settings Page
        self.ui.addRouterBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.AddRouter))
        
        self.ui.usersBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.createUserPage))
        
        self.ui.searchUserBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        self.ui.navBar.clicked.connect(self.toggle_sidebar)
        self.loadAllEmployeesGraph()

        # Initialize sidebar state (visible)
        self.sidebar_visible = False
        # self.plotCircularGraph()

    # def plotCircularGraph(self):
    #     # Create circular data
    #     theta = np.linspace(0, 2 * np.pi, 100)
    #     x = 10 * np.cos(theta)
    #     y = 10 * np.sin(theta)

    #     # Plot the circular graph
    #     self.ui.graphicsView.clear()  # Clear existing plots
    #     self.ui.graphicsView.plot(x, y, pen='b', symbol='o', symbolPen='b', symbolBrush=0.2, name='Circular Plot')

        

    
    def onTitleBarMousePress(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def onTitleBarMouseMove(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def close_application(self):
        # Handle the close action here
        self.close()

    def resize_application(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
    def minimize_application(self):
        self.showMinimized()
        # Connect signals and slots (add your custom logic here)
        # self.ui.pushButton.clicked.connect(self.on_button_click)

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
        self.ui.addRouterBtn.setText("Add Router" if self.sidebar_visible else "")
        self.ui.usersBtn.setText("Users" if self.sidebar_visible else "")
        self.ui.searchUserBtn.setText("Search User" if self.sidebar_visible else "")
        # self.ui.navBar.setText(">" if self.sidebar_visible else "<")
        self.ui.searchUserBtn_2.setText("Generate" if self.sidebar_visible else "")
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
        

def main():

    app = QApplication(sys.argv)
    # loginWindow=LoginPageUI()
    # loginWindow.show()
    window = MainUIClass()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
