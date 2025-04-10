import unittest
from dao.lease_repo_impl import ICarLeaseRepositoryImpl
from exception.car_not_found_exception import CarNotFoundException
from exception.customer_not_found_exception import CustomerrNotFoundException
from exception.lease_not_found_exception import LeaseNotFoundException

class TestExceptionHandling(unittest.TestCase):
    def setUp(self):
        self.repo = ICarLeaseRepositoryImpl()

    def test_car_not_found(self):
        with self.assertRaises(CarNotFoundException):
            self.repo.findCarById(-1)

    def test_customer_not_found(self):
        with self.assertRaises(CustomerrNotFoundException):
            self.repo.findCustomerById(-1)

    def test_lease_not_found(self):
        with self.assertRaises(LeaseNotFoundException):
            self.repo.returnCar(-1)

if __name__ == '__main__':
    unittest.main()
