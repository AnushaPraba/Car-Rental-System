import unittest
from dao.lease_repo_impl import ICarLeaseRepositoryImpl
from entity.car import Vehicle

class TestVehicleFunctions(unittest.TestCase):
    def setUp(self):
        self.repo = ICarLeaseRepositoryImpl()

    def test_add_car_success(self):
        car = Vehicle(None, "TestMake", "TestModel", 2024, 75.0, "available", 4, 2.2)
        self.repo.addCar(car)
        cars = self.repo.listAvailableCars()
        self.assertTrue(any(c.get_make() == "TestMake" and c.get_model() == "TestModel" for c in cars))

if __name__ == '__main__':
    unittest.main()
