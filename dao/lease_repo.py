from abc import ABC, abstractmethod
from typing import List
from entity.car import Vehicle
from entity.customer import Customer
from entity.lease import Lease

class ICarLeaseRepository(ABC):

    # --- Car Management ---
    @abstractmethod
    def addCar(self, car: Vehicle) -> None:
        pass

    @abstractmethod
    def removeCar(self, carID: int) -> None:
        pass

    @abstractmethod
    def listAvailableCars(self) -> List[Vehicle]:
        pass

    @abstractmethod
    def listRentedCars(self) -> List[Vehicle]:
        pass

    @abstractmethod
    def findCarById(self, carID: int) -> Vehicle:
        pass

    # --- Customer Management ---
    @abstractmethod
    def isEmailOrPhoneExists(self, email: str, phone: str) -> bool:
        pass

    @abstractmethod
    def addCustomer(self, customer: Customer) -> None:
        pass

    @abstractmethod
    def removeCustomer(self, customerID: int) -> None:
        pass

    @abstractmethod
    def updateCustomer(self, customer: Customer):
        pass

    @abstractmethod
    def listCustomers(self) -> List[Customer]:
        pass

    @abstractmethod
    def findCustomerById(self, customerID: int) -> Customer:
        pass

    # --- Lease Management ---
    @abstractmethod
    def createLease(self, customerID: int, carID: int, startDate, endDate) -> Lease:
        pass

    @abstractmethod
    def returnCar(self, leaseID: int) -> Lease:
        pass

    @abstractmethod
    def listActiveLeases(self) -> List[Lease]:
        pass

    @abstractmethod
    def listLeaseHistory(self):
        pass

    @abstractmethod
    def findLeaseById(self, lease_id: int) -> Lease:
        pass

    @abstractmethod
    def recordPayment(self, lease: Lease, amount: float) -> None:
        pass
