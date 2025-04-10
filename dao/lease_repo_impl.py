from typing import List
from dao.lease_repo import ICarLeaseRepository
from entity.car import Vehicle
from entity.customer import Customer
from entity.lease import Lease
from util.db_conn_util import DBConnUtil
from exception.lease_not_found_exception import LeaseNotFoundException
from exception.car_not_found_exception import CarNotFoundException
from exception.customer_not_found_exception import CustomerrNotFoundException

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
        cursor.execute("DELETE FROM Vehicle WHERE vehicleID = %s", (carID,))
        self.conn.commit()

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
            raise CarNotFoundException("Car not found")

    # --- Customer Management ---
    def addCustomer(self, customer: Customer) -> None:
        cursor = self.conn.cursor()
        sql = "INSERT INTO Customer (firstName, lastName, email, phoneNumber) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (customer.get_firstName(), customer.get_lastName(),
                             customer.get_email(), customer.get_phoneNumber()))
        self.conn.commit()

    def removeCustomer(self, customerID: int) -> None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Customer WHERE customerID = %s", (customerID,))
        self.conn.commit()

    def updateCustomer(self, customer: Customer):
        cursor = self.conn.cursor()
        try:
            query = """UPDATE Customer 
                       SET firstName=%s, lastName=%s, email=%s, phoneNumber=%s 
                       WHERE customerID=%s"""
            cursor.execute(query, (
            customer.get_firstName(), customer.get_lastName(), customer.get_email(), customer.get_phoneNumber(), customer.get_customerID()))
            self.conn.commit()
            if cursor.rowcount == 0:
                raise CustomerrNotFoundException(f"Customer with ID {customer.get_customerID()} not found.")
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
            raise CustomerrNotFoundException("Customer not found")

    # --- Lease Management ---
    def createLease(self, customerID: int, carID: int, startDate, endDate) -> Lease:
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO Lease (vehicleID, customerID, startDate, endDate, type)
            VALUES (%s, %s, %s, %s, %s)
        """, (carID, customerID, startDate, endDate, 'DailyLease'))
        self.conn.commit()
        lease_id = cursor.lastrowid
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

    def listLeaseHistory(self) -> List[Lease]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Lease")
        rows = cursor.fetchall()
        return [Lease(*row) for row in rows]

    # --- Payment Handling ---
    def recordPayment(self, lease: Lease, amount: float) -> None:
        cursor = self.conn.cursor()
        sql = "INSERT INTO Payment (leaseID, paymentDate, amount) VALUES (%s,curdate(), %s)"
        cursor.execute(sql, (lease.get_leaseID(), amount))
        self.conn.commit()
