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



class LoginPageUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create an instance of the generated UI class
        self.ui = logi()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(self.logn_successful)

    def logn_successful(self):
        self.open_landing_page

    def open_landing_page(self):
        self.landing_form = MainUIClass()
        self.hide()
        time.sleep(0.2)
        self.landing_form.show()
    
    
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
        self.plotCircularGraph()

    def plotCircularGraph(self):
        # Create circular data
        theta = np.linspace(0, 2 * np.pi, 100)
        x = 10 * np.cos(theta)
        y = 10 * np.sin(theta)

        # Plot the circular graph
        self.ui.graphicsView.clear()  # Clear existing plots
        self.ui.graphicsView.plot(x, y, pen='b', symbol='o', symbolPen='b', symbolBrush=0.2, name='Circular Plot')

        

    
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
        

def main():
    app = QApplication(sys.argv)
    # loginWindow=LoginPageUI()
    # loginWindow.show()
    window = MainUIClass()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
