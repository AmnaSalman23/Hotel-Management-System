import sqlite3
from contextlib import closing
import datetime
from PyQt5.QtWidgets import QMessageBox
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
        
    def add_reservation(self, customer_id, room_number, check_in_date, check_out_date):
        query = '''
            INSERT INTO Reservations (CustomerID, RoomNumber, CheckInDate, CheckOutDate)
            VALUES (?, ?, ?, ?)
        '''
        try:
            self.execute_query(query, (customer_id, room_number, check_in_date, check_out_date))
            return True  # Successful reservation
        except sqlite3.IntegrityError:
            return False
    def show_all_reservations(self):
        query = '''
            SELECT *
            FROM Reservations
        '''
        return self.fetch_all(query)
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

    def add_guest_with_room(self, first_name, last_name, email, phone_number, address, nationality, check_in_date, check_out_date, room_number, room_type):
        try:
            # Insert new guest into Guests Table
            self.execute_query('''
                INSERT INTO Guests (first_name, last_name, email, phone_number, address, nationality, check_in_date, check_out_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (first_name, last_name, email, phone_number, address, nationality, check_in_date, check_out_date))

            # Get the guest_id of the newly added guest
            guest_id = self.fetch_one("SELECT last_insert_rowid()")[0]

            # Get the room_id based on the provided room_number and room_type
            room_id = self.fetch_one('''
                SELECT room_id FROM Rooms WHERE room_number = ? AND room_type = ?
            ''', (room_number, room_type))[0]

            # Insert reservation into Reservations Table
            self.execute_query('''
                INSERT INTO Reservations (guest_id, room_id, check_in_date, check_out_date, reservation_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (guest_id, room_id, check_in_date, check_out_date, datetime.date.today()))

            # Update the availability status of the room
            self.execute_query('''
                UPDATE Rooms SET availability_status = 'Occupied' WHERE room_id = ?
            ''', (room_id,))

            return True  # Successful guest addition and room assignment

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False  # Failed to add guest and assign room
        
    def delete_guest(self, guest_id):
        try:
            # Check if the guest exists
            existing_guest = self.fetch_one('SELECT * FROM Guests WHERE guest_id = ?', (guest_id,))
            if not existing_guest:
                print(f"Error: Guest with ID {guest_id} not found.")
                return False

            # Get the room_id associated with the guest
            room_id = self.fetch_one('SELECT room_id FROM Reservations WHERE guest_id = ?', (guest_id,))
            if room_id:
                room_id = room_id[0]

                # Update the availability status of the room
                self.execute_query('UPDATE Rooms SET availability_status = "Available" WHERE room_id = ?', (room_id,))

                # Delete the reservation associated with the guest
                self.execute_query('DELETE FROM Reservations WHERE guest_id = ?', (guest_id,))
            else:
                print(f"Error: No reservation found for Guest with ID {guest_id}.")

            # Delete the guest from the Guests table
            self.execute_query('DELETE FROM Guests WHERE guest_id = ?', (guest_id,))

            return True  # Successful guest deletion

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False  # Failed to delete guest

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
