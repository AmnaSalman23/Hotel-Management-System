import sqlite3
from datetime import date

def create_database():
    # Connect to the SQLite database (or create a new one if it doesn't exist)
    conn = sqlite3.connect('hotel_management.db')
    cursor = conn.cursor()

    # Check if the tables already exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    existing_tables = cursor.fetchall()
    existing_table_names = [table[0] for table in existing_tables]

    if 'Guests' in existing_table_names:
        print("Tables already exist. Skipping creation.")
        conn.close()
        return

    # Create Guests Table
    cursor.execute('''
        CREATE TABLE Guests (
            guest_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone_number TEXT,
            address TEXT,
            nationality TEXT,
            check_in_date DATE,
            check_out_date DATE
        )
    ''')

    # Insert sample data into Guests Table
    cursor.execute('''
        INSERT INTO Guests (first_name, last_name, email, phone_number, address, nationality, check_in_date, check_out_date)
        VALUES ('John', 'Doe', 'john.doe@example.com', '123456789', '123 Main St', 'USA', '2023-01-01', '2023-01-10')
    ''')

    # Create Rooms Table
    cursor.execute('''
        CREATE TABLE Rooms (
            room_id INTEGER PRIMARY KEY,
            room_number INTEGER,
            room_type TEXT,
            occupancy_limit INTEGER,
            availability_status TEXT
        )
    ''')

    # Insert sample data into Rooms Table
    cursor.execute('''
        INSERT INTO Rooms (room_number, room_type, occupancy_limit, availability_status)
        VALUES (101, 'Standard', 2, 'Available'),
               (102, 'Suite', 4, 'Available')
    ''')

    # Create Reservations Table
    cursor.execute('''
        CREATE TABLE Reservations (
            reservation_id INTEGER PRIMARY KEY,
            guest_id INTEGER,
            room_id INTEGER,
            check_in_date DATE,
            check_out_date DATE,
            reservation_date DATE,
            FOREIGN KEY (guest_id) REFERENCES Guests(guest_id),
            FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
        )
    ''')

    # Insert sample data into Reservations Table
    cursor.execute('''
        INSERT INTO Reservations (guest_id, room_id, check_in_date, check_out_date, reservation_date)
        VALUES (1, 101, '2023-01-01', '2023-01-10', '2023-01-01')
    ''')

    # Create Services Table
    cursor.execute('''
        CREATE TABLE Services (
            service_id INTEGER PRIMARY KEY,
            service_name TEXT,
            description TEXT,
            price INTEGER
        )
    ''')

    # Insert sample data into Services Table
    cursor.execute('''
        INSERT INTO Services (service_name, description, price)
        VALUES ('Room Service', 'In-room dining', 20),
               ('Laundry', 'Washing and folding', 15)
    ''')

    # Create Orders Table
    cursor.execute('''
        CREATE TABLE Orders (
            order_id INTEGER PRIMARY KEY,
            guest_id INTEGER,
            service_id INTEGER,
            order_date DATE,
            quantity INTEGER,
            total_amount INTEGER,
            FOREIGN KEY (guest_id) REFERENCES Guests(guest_id),
            FOREIGN KEY (service_id) REFERENCES Services(service_id)
        )
    ''')

    # Insert sample data into Orders Table
    cursor.execute('''
        INSERT INTO Orders (guest_id, service_id, order_date, quantity, total_amount)
        VALUES (1, 1, '2023-01-02', 2, 40),
               (1, 2, '2023-01-03', 1, 15)
    ''')

    # Create Employees Table
    cursor.execute('''
        CREATE TABLE Employees (
            employee_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone_number TEXT,
            position TEXT,
            salary INTEGER
        )
    ''')

    # Insert sample data into Employees Table
    cursor.execute('''
        INSERT INTO Employees (first_name, last_name, email, phone_number, position, salary)
        VALUES ('Alice', 'Smith', 'alice.smith@example.com', '987654321', 'Receptionist', 50000),
               ('Bob', 'Jones', 'bob.jones@example.com', '555666777', 'Housekeeper', 40000)
    ''')

    # Create Users Table
    cursor.execute('''
        CREATE TABLE Users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            email TEXT,
            password TEXT,
            role TEXT,
            # guest_id INTEGER,
            # employee_id INTEGER,
            # reservation_id INTEGER,
            # FOREIGN KEY (guest_id) REFERENCES Guests(guest_id),
            # FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
            # FOREIGN KEY (reservation_id) REFERENCES Reservations(reservation_id)
        )
    ''')

    # Insert sample data into Users Table
    cursor.execute('''
        INSERT INTO Users (username, email, password, role, guest_id, employee_id, reservation_id)
        VALUES ('user1', 'user1@example.com', 'password1', 'guest', 1, NULL, 1),
               ('user2', 'user2@example.com', 'password2', 'employee', NULL, 1, NULL)
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Call the function to create the database
create_database()
