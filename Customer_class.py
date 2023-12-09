
from PyQt5.QtWidgets import QMainWindow
import time
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon
from customer_landing_page import Ui_MainWindow as cust
# from admin_landing_page import Ui_MainWindow as admin
from show_messages import show_error_message, show_success_message
# from signup_class import SignUpPageUI


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
        show_error_message(self, "Room booked successfully!")

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
        self.login_form = LoginPageUI()
        self.hide()
        time.sleep(0.2)
        self.login_form.show()

    def open_signup_page(self):
        self.signup_form = SignUpPageUI()
        self.hide()
        time.sleep(0.2)
        self.signup_form.show()