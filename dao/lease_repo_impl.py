from dao.lease_repo import ICarLeaseRepository
from entity.car import Vehicle
from entity.customer import Customer
from entity.lease import Lease
from util.db_conn_util import DBConnUtil
from exception.lease_not_found_exception import LeaseNotFoundException
from exception.car_not_found_exception import CarNotFoundException
from exception.customer_not_found_exception import CustomerrNotFoundException
from exception.invalid_customer_detail_exception import DuplicateCustomerException
import mysql.connector
from datetime import date

class ICarLeaseRepositoryImpl(ICarLeaseRepository):

    def __init__(self):
        self.conn = DBConnUtil.get_connection(r'C:/Users/anush/PycharmProjects/Car Rental System/util/db.properties')

    # --- Car Management ---
    def addCar(self, car: Vehicle) -> None:
        cursor = self.conn.cursor()
        sql = """
            INSERT INTO Vehicle (make, model, year, dailyRate, status, passengerCapacity, engineCapacity)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (car.get_make(), car.get_model(), car.get_year(), car.get_dailyRate(),
                             car.get_status(), car.get_passengerCapacity(), car.get_engineCapacity()))
        self.conn.commit()

    def removeCar(self, carID: int) -> None:
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM Vehicle WHERE vehicleID = %s", (carID,))
        car = cursor.fetchone()
        if car is None:
            raise CarNotFoundException(f"Car with ID {carID} does not exist.")

        if car[5] != 'available':
            raise Exception("Cannot remove car. It is currently not available (still leased or reserved).")

        try:
            cursor.execute("DELETE FROM Vehicle WHERE vehicleID = %s", (carID,))
            self.conn.commit()
            print(f"Car with ID {carID} removed successfully.")
        except mysql.connector.Error as e:
            if e.errno == 1451:
                cursor.execute("UPDATE Vehicle SET status = 'notAvailable' WHERE vehicleID = %s", (carID,))
                self.conn.commit()
                print(f"Car with ID {carID} could not be deleted as it is referenced in records. Status set to 'notAvailable'.")
            else:
                raise e

    def listAvailableCars(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Vehicle WHERE status = 'available'")
        rows = cursor.fetchall()
        return [row for row in rows]

    def listRentedCars(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Vehicle WHERE status = 'notAvailable'")
        rows = cursor.fetchall()
        return [row for row in rows]

    def findCarById(self, carID: int) -> Vehicle:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Vehicle WHERE vehicleID = %s", (carID,))
        row = cursor.fetchone()
        if row:
            return Vehicle(*row)
        else:
            raise CarNotFoundException("Car not found for the given ID")

    # --- Customer Management ---
    def addCustomer(self, customer: Customer):
        cursor = self.conn.cursor()
        sql = "INSERT INTO Customer (firstName, lastName, email, phoneNumber) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (customer.get_firstName(), customer.get_lastName(),
                             customer.get_email(), customer.get_phoneNumber()))
        customer_id = cursor.lastrowid
        self.conn.commit()
        return customer_id

    def addUser(self, username, hashed_password, role, customer_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, password, role, customerID)
            VALUES (%s, %s, %s, %s)
        """, (username, hashed_password, role, customer_id))
        self.conn.commit()

    def isEmailOrPhoneExists(self, email: str, phone: str, customer_id: int = None) -> bool:
        cursor = self.conn.cursor()
        if customer_id:
            query = """
                SELECT COUNT(*) FROM Customer
                WHERE (email = %s OR phoneNumber = %s) AND customerID != %s
            """
            cursor.execute(query, (email, phone, customer_id))
        else:
            query = "SELECT COUNT(*) FROM Customer WHERE email = %s OR phoneNumber = %s"
            cursor.execute(query, (email, phone))
        result = cursor.fetchone()
        return result[0] > 0

    def removeCustomer(self, customerID: int) -> None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Customer WHERE customerID = %s", (customerID,))
        customer = cursor.fetchone()

        if customer is None:
            raise CustomerrNotFoundException(f"Customer with ID {customerID} does not exist.")

        try:
            cursor.execute("SELECT * FROM Lease WHERE customerID = %s", (customerID,))
            lease = cursor.fetchone()
            if lease:
                raise Exception("Cannot remove customer. They are associated with an existing lease.")

            cursor.execute("DELETE FROM Users WHERE customerID = %s", (customerID,))
            cursor.execute("DELETE FROM Customer WHERE customerID = %s", (customerID,))
            self.conn.commit()
            print(f"Customer with ID {customerID} removed successfully.")

        except Exception as e:
            print(e)

    def updateCustomer(self, customer: Customer):
        cursor = self.conn.cursor()
        try:
            query = """UPDATE Customer 
                       SET firstName=%s, lastName=%s, email=%s, phoneNumber=%s 
                       WHERE customerID=%s"""
            cursor.execute(query, (
            customer.get_firstName(), customer.get_lastName(), customer.get_email(), customer.get_phoneNumber(), customer.get_customerID()))
            self.conn.commit()

        finally:
            cursor.close()
            self.conn.close()

    def listCustomers(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Customer")
        rows = cursor.fetchall()
        return [row for row in rows]

    def findCustomerById(self, customerID: int) -> Customer:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Customer WHERE customerID = %s", (customerID,))
        row = cursor.fetchone()
        if row:
            return Customer(*row)
        else:
            raise CustomerrNotFoundException("Customer not found with the given ID")

    def createLease(self, customerID: int, carID: int, startDate, endDate) -> Lease:
        cursor = self.conn.cursor()

        today = date.today()
        if startDate < today:
            raise ValueError("Start date cannot be in the past.")
        if endDate < startDate:
            raise ValueError("End date cannot be earlier than start date.")

        cursor.execute("SELECT * FROM Customer WHERE customerID = %s", (customerID,))
        if cursor.fetchone() is None:
            raise CustomerrNotFoundException(f"Customer with ID {customerID} not found.")

        cursor.execute("SELECT * FROM Vehicle WHERE vehicleID = %s AND status = 'available'", (carID,))
        if cursor.fetchone() is None:
            raise CarNotFoundException(f"Car with ID {carID} not found or not available.")

        totaldays = (endDate - startDate).days + 1
        expectedAmount = totaldays * (cursor.execute("SELECT dailyRate FROM Vehicle WHERE vehicleID = %s", (carID,)))

        cursor.execute("""
            INSERT INTO Lease (vehicleID, customerID, startDate, endDate, type,expectedAmount)
            VALUES (%s, %s, %s, %s, %s,%s)
        """, (carID, customerID, startDate, endDate, 'DailyLease',expectedAmount))
        self.conn.commit()
        lease_id = cursor.lastrowid

        # Mark the car as not available
        cursor.execute("UPDATE Vehicle SET status = 'notAvailable' WHERE vehicleID = %s", (carID,))
        self.conn.commit()

        return Lease(lease_id, carID, customerID, startDate, endDate, 'DailyLease',expectedAmount)

    def returnCar(self, leaseID: int) -> Lease:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Lease WHERE leaseID = %s", (leaseID,))
        row = cursor.fetchone()
        if not row:
            raise LeaseNotFoundException("Lease not found")
        lease = Lease(*row)
        cursor.execute("UPDATE Vehicle SET status = 'available' WHERE vehicleID = %s", (lease.get_vehicleID(),))
        self.conn.commit()
        return lease

    def listActiveLeases(self):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT 
                l.leaseID,
                c.customerID,
                    CONCAT(c.firstName, ' ', c.lastName) AS customerName,
                    c.phoneNumber,
                    v.vehicleID,
                    v.model,
                    v.dailyRate,
                    l.startDate, l.endDate,
                    DATEDIFF(l.endDate, l.startDate) + 1 AS totalDays,
                    l.expectedAmount,l.paymentStatus
        FROM Lease l
        JOIN Customer c ON l.customerID = c.customerID
        JOIN Vehicle v ON l.vehicleID = v.vehicleID
        WHERE l.endDate >= CURDATE()""")
        rows = cursor.fetchall()
        return [row for row in rows]

    def listLeaseHistory(self):
        cursor = self.conn.cursor()
        query = """
                SELECT 
                l.leaseID,
                c.customerID,
                    CONCAT(c.firstName, ' ', c.lastName) AS customerName,
                    c.phoneNumber,
                    v.vehicleID,
                    v.model,
                    v.dailyRate,
                    l.startDate, l.endDate,
                    DATEDIFF(l.endDate, l.startDate) + 1 AS totalDays,
                    l.expectedAmount,l.paymentStatus
                FROM Lease l
                JOIN Customer c ON l.customerID = c.customerID
                JOIN Vehicle v ON l.vehicleID = v.vehicleID
            """
        cursor.execute(query)
        rows= cursor.fetchall()
        return [row for row in rows]

    def listLeasesByCustomer(self, customerID: int):
        cursor=self.conn.cursor()
        cursor.execute("""SELECT l.leaseID,v.vehicleID, v.model, v.dailyRate, l.startDate, l.endDate,
        DATEDIFF(l.endDate, l.startDate) + 1 AS totalDays,l.expectedAmount,l.paymentStatus
        FROM Lease l
        JOIN Vehicle v ON l.vehicleID = v.vehicleID
        WHERE l.customerID = %s
        ORDER BY l.startDate DESC
        """, (customerID,))
        rows = cursor.fetchall()
        return [row for row in rows]

    def get_payment_history(self):
        cursor = self.conn.cursor()
        cursor.execute("""
                    SELECT 
                        p.paymentID,
                        p.leaseID,
                        v.vehicleID,
                        c.customerID,
                        CONCAT(c.firstName, ' ', c.lastName) AS customerName,
                        p.paymentDate,
                        p.amount,
                        l.expectedAmount,
                        l.paymentStatus
                    FROM 
                        payment p
                    JOIN 
                        lease l ON p.leaseID = l.leaseID
                    JOIN
                        customer c ON l.customerID = c.customerID
                    JOIN 
                        vehicle v ON l.vehicleID = v.vehicleID
                    ORDER BY 
                        p.paymentDate DESC
                """)
        rows = cursor.fetchall()
        return [row for row in rows]

    def findLeaseById(self, lease_id: int) -> Lease:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Lease WHERE leaseID = %s", (lease_id,))
        row = cursor.fetchone()

        if row:
            return Lease(*row)
        else:
            raise LeaseNotFoundException(f"Lease with ID {lease_id} not found.")

    def recordPayment(self, lease: Lease, amount: float) -> None:
        cursor = self.conn.cursor()

        # Validate lease exists
        cursor.execute("SELECT expectedAmount, paymentStatus FROM Lease WHERE leaseID = %s", (lease.get_leaseID(),))
        lease_data = cursor.fetchone()
        if not lease_data:
            raise LeaseNotFoundException(f"Lease with ID {lease.get_leaseID()} not found.")

        expected_amount, payment_status = lease_data

        if payment_status.lower() == 'paid':
            raise Exception(f"Lease with ID {lease.get_leaseID()} has already been paid.")

        if amount != expected_amount:
            raise Exception(f"Invalid payment amount. Expected: {expected_amount}, but received: {amount}")

        cursor.execute("""
            INSERT INTO Payment (leaseID, paymentDate, amount)
            VALUES (%s, CURDATE(), %s)
        """, (lease.get_leaseID(), amount))

        cursor.execute("UPDATE Lease SET paymentStatus = 'Paid' WHERE leaseID = %s", (lease.get_leaseID(),))
        self.conn.commit()

    def get_payment_history_by_customer(self, customerID):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                p.paymentID,
                p.leaseID,
                v.vehicleID,
                p.paymentDate,
                p.amount,
                l.expectedAmount,
                l.paymentStatus
            FROM 
                payment p
            JOIN 
                lease l ON p.leaseID = l.leaseID
            JOIN 
                vehicle v ON l.vehicleID = v.vehicleID
            WHERE 
                l.customerID = %s
            ORDER BY 
                p.paymentDate DESC
        """, (customerID,))
        rows =cursor.fetchall()
        return [row for row in rows]

    def is_username_unique(self,username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        if cursor.fetchone() is None:
            return True
        else:
            raise DuplicateCustomerException("Username already exists. Choose another.")

