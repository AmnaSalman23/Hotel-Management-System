import sqlite3

# Function to create the SQLite database and tables
def create_database():
    # Connect to the SQLite database (creates a new database if it doesn't exist)
    connection = sqlite3.connect("hotel_management.db")
    cursor = connection.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            CustomerID INTEGER PRIMARY KEY,
            FirstName TEXT,
            LastName TEXT,
            PhoneNumber TEXT,
            Feedback TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Rooms (
            RoomNumber INTEGER PRIMARY KEY,
            Occupants INTEGER,
            DefaultRate REAL,
            Assured BOOLEAN
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reservations (
            ReservationID INTEGER PRIMARY KEY,
            CustomerID INTEGER,
            RoomNumber INTEGER,
            CheckInDateTime TEXT,
            CheckOutDateTime TEXT,
            IsAssured BOOLEAN,
            ConfirmationNumber TEXT,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
            FOREIGN KEY (RoomNumber) REFERENCES Rooms(RoomNumber)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Meals (
            MealID INTEGER PRIMARY KEY,
            Description TEXT,
            Price REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MealOrders (
            OrderID INTEGER PRIMARY KEY,
            CustomerID INTEGER,
            MealID INTEGER,
            PaymentType TEXT,
            IsPaid BOOLEAN,
            ReservationID INTEGER,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
            FOREIGN KEY (MealID) REFERENCES Meals(MealID),
            FOREIGN KEY (ReservationID) REFERENCES Reservations(ReservationID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Services (
            ServiceID INTEGER PRIMARY KEY,
            ServiceName TEXT,
            Description TEXT,
            Price REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            UserID INTEGER PRIMARY KEY,
            Username TEXT UNIQUE,
            Password TEXT,
            Email TEXT UNIQUE,
            UserType TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS HotelOccupancy (
            Date TEXT PRIMARY KEY,
            Occupancy INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AccessLevels (
            AccessLevelID INTEGER PRIMARY KEY,
            UserType TEXT,
            CanManageStaff BOOLEAN,
            CanManageServices BOOLEAN,
            CanManageBookings BOOLEAN,
            CanManagePayments BOOLEAN,
            CanGenerateReports BOOLEAN
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UserAccess (
            UserID INTEGER,
            AccessLevelID INTEGER,
            FOREIGN KEY (UserID) REFERENCES Users(UserID),
            FOREIGN KEY (AccessLevelID) REFERENCES AccessLevels(AccessLevelID)
        )
    ''')

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

# Call the function to create the database
create_database()
