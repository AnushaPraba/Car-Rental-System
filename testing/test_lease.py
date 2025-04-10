import unittest
from dao.lease_repo_impl import ICarLeaseRepositoryImpl
from entity.car import Vehicle
from entity.customer import Customer
from datetime import date

class TestLeaseFunctions(unittest.TestCase):
    def setUp(self):
        self.repo = ICarLeaseRepositoryImpl()

    def test_create_lease_success(self):
        customer = Customer(None, "Lease", "User", "lease@example.com", "9876543210")
        self.repo.addCustomer(customer)
        customer_id = self.repo.listCustomers()[-1].get_customerID()

        car = Vehicle(None, "LeaseMake", "LeaseModel", 2023, 90.0, "available", 4, 2.0)
        self.repo.addCar(car)
        car_id = self.repo.listAvailableCars()[-1].get_vehicleID()

        lease = self.repo.createLease(customer_id, car_id, date.today(), date.today())
        self.assertIsNotNone(lease)

if __name__ == '__main__':
    unittest.main()
