import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QApplication
import sqlite3
from login_page_class import LoginPageUI






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
            INSERT INTO Users (Username, Password, Email, Role)
            VALUES (?, ?, ?, ?)
        '''
        try:
            self.execute_query(query, (username, password, email, user_type))
            return True  # Successful registration
        except sqlite3.IntegrityError:
            return False  # User with the same username or email already exists
    def get_user_role(self, username, password):
        query = '''
            SELECT Role
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


def main():

    try:
        app = QApplication(sys.argv)
        window=LoginPageUI(DatabaseManager("hotel_management.db"))
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
