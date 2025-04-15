from typing import List
from dao.lease_repo import ICarLeaseRepository
from entity.car import Vehicle
from entity.customer import Customer
from entity.lease import Lease
from util.db_conn_util import DBConnUtil
from exception.lease_not_found_exception import LeaseNotFoundException
from exception.car_not_found_exception import CarNotFoundException
from exception.customer_not_found_exception import CustomerrNotFoundException
import mysql.connector


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

    # def removeCar(self, carID: int) -> None:
    #     cursor = self.conn.cursor()
    #     cursor.execute("DELETE FROM Vehicle WHERE vehicleID = %s", (carID,))
    #     self.conn.commit()
    #
    # def removeCar(self, carID: int) -> None:
    #     cursor = self.conn.cursor()
    #     cursor.execute("SELECT * FROM Vehicle WHERE vehicleID = %s", (carID,))
    #     car = cursor.fetchone()
    #
    #     if car is None:
    #         raise CarNotFoundException(f"Car with ID {carID} does not exist.")
    #     else:
    #         cursor.execute("DELETE FROM Vehicle WHERE vehicleID = %s", (carID,))
    #         self.conn.commit()

    def removeCar(self, carID: int) -> None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Vehicle WHERE vehicleID = %s", (carID,))
        car = cursor.fetchone()

        if car is None:
            raise CarNotFoundException(f"Car with ID {carID} does not exist.")

        try:
            cursor.execute("DELETE FROM Vehicle WHERE vehicleID = %s", (carID,))
            self.conn.commit()
        except mysql.connector.Error as e:
            if e.errno == 1451:
                raise Exception("Cannot remove car. It is linked to an active lease.")
            else:
                raise e

    def listAvailableCars(self) -> List[Vehicle]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Vehicle WHERE status = 'available'")
        rows = cursor.fetchall()
        # return [row for row in rows]
        return [Vehicle(*row) for row in rows]

    def listRentedCars(self) -> List[Vehicle]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Vehicle WHERE status = 'notAvailable'")
        rows = cursor.fetchall()
        return [Vehicle(*row) for row in rows]

    def findCarById(self, carID: int) -> Vehicle:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Vehicle WHERE vehicleID = %s", (carID,))
        row = cursor.fetchone()
        if row:
            return Vehicle(*row)
        else:
            raise CarNotFoundException("Car not found for the given ID")

    # --- Customer Management ---
    def addCustomer(self, customer: Customer) -> None:
        cursor = self.conn.cursor()
        sql = "INSERT INTO Customer (firstName, lastName, email, phoneNumber) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (customer.get_firstName(), customer.get_lastName(),
                             customer.get_email(), customer.get_phoneNumber()))
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

    #
    # def removeCustomer(self, customerID: int) -> None:
    #     cursor = self.conn.cursor()
    #     cursor.execute("DELETE FROM Customer WHERE customerID = %s", (customerID,))
    #     self.conn.commit()

    def removeCustomer(self, customerID: int) -> None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Customer WHERE customerID = %s", (customerID,))
        customer = cursor.fetchone()

        if customer is None:
            raise CustomerrNotFoundException(f"Customer with ID {customerID} does not exist.")

        try:
            cursor.execute("DELETE FROM Customer WHERE customerID = %s", (customerID,))
            self.conn.commit()
        except mysql.connector.Error as e:
            if e.errno == 1451:
                raise Exception("Cannot remove customer. They are associated with an existing lease.")
            else:
                raise e

    def updateCustomer(self, customer: Customer):
        cursor = self.conn.cursor()
        try:
            query = """UPDATE Customer 
                       SET firstName=%s, lastName=%s, email=%s, phoneNumber=%s 
                       WHERE customerID=%s"""
            cursor.execute(query, (
            customer.get_firstName(), customer.get_lastName(), customer.get_email(), customer.get_phoneNumber(), customer.get_customerID()))
            self.conn.commit()
            # if cursor.rowcount == 0:
            #     raise CustomerrNotFoundException(f"Customer with ID {customer.get_customerID()} not found.")
        finally:
            cursor.close()
            self.conn.close()

    def listCustomers(self) -> List[Customer]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Customer")
        rows = cursor.fetchall()
        return [Customer(*row) for row in rows]

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

        # Check if customer exists
        cursor.execute("SELECT * FROM Customer WHERE customerID = %s", (customerID,))
        if cursor.fetchone() is None:
            raise CustomerrNotFoundException(f"Customer with ID {customerID} not found.")

        # Check if car exists and is available
        cursor.execute("SELECT * FROM Vehicle WHERE vehicleID = %s AND status = 'available'", (carID,))
        if cursor.fetchone() is None:
            raise CarNotFoundException(f"Car with ID {carID} not found or not available.")

        # Proceed with lease creation
        cursor.execute("""
            INSERT INTO Lease (vehicleID, customerID, startDate, endDate, type)
            VALUES (%s, %s, %s, %s, %s)
        """, (carID, customerID, startDate, endDate, 'DailyLease'))
        self.conn.commit()
        lease_id = cursor.lastrowid

        # Mark the car as not available
        cursor.execute("UPDATE Vehicle SET status = 'notAvailable' WHERE vehicleID = %s", (carID,))
        self.conn.commit()

        return Lease(lease_id, carID, customerID, startDate, endDate, 'DailyLease')

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

    def listActiveLeases(self) -> List[Lease]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Lease WHERE endDate >= CURDATE()")
        rows = cursor.fetchall()
        return [Lease(*row) for row in rows]

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
                    (DATEDIFF(l.endDate, l.startDate) + 1) * v.dailyRate AS expectedAmount
                FROM Lease l
                JOIN Customer c ON l.customerID = c.customerID
                JOIN Vehicle v ON l.vehicleID = v.vehicleID
            """
        cursor.execute(query)
        return cursor.fetchall()

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
        cursor.execute("SELECT * FROM Lease WHERE leaseID = %s", (lease.get_leaseID(),))
        lease_row = cursor.fetchone()
        if not lease_row:
            raise LeaseNotFoundException(f"Lease with ID {lease.get_leaseID()} not found.")

        # Fetch car rate
        vehicle_id = lease.get_vehicleID()
        cursor.execute("SELECT dailyRate FROM Vehicle WHERE vehicleID = %s", (vehicle_id,))
        rate_row = cursor.fetchone()
        if not rate_row:
            raise Exception(f"Rate for vehicle ID {vehicle_id} not found.")
        daily_rate = rate_row[0]

        # Calculate number of days
        start = lease.get_startDate()
        end = lease.get_endDate()
        duration = (end - start).days + 1  # Include both start and end dates

        expected_amount = duration * daily_rate

        # Compare expected and entered amount
        if amount != expected_amount:
            raise Exception(f"Invalid payment amount. Expected: {expected_amount}, but received: {amount}")

        # Record payment
        cursor.execute("""
            INSERT INTO Payment (leaseID, paymentDate, amount)
            VALUES (%s, CURDATE(), %s)
        """, (lease.get_leaseID(), amount))
        self.conn.commit()
