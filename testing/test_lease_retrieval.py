import unittest
from dao.lease_repo_impl import ICarLeaseRepositoryImpl

class TestLeaseRetrieval(unittest.TestCase):
    def setUp(self):
        self.repo = ICarLeaseRepositoryImpl()

    def test_retrieve_leases_success(self):
        leases = self.repo.listActiveLeases()  # or listLeaseHistory() if that's what you want
        self.assertIsInstance(leases, list)
        # Optionally check if leases contain expected attributes
        if leases:
            self.assertTrue(hasattr(leases[0], "get_leaseID"))

if __name__ == '__main__':
    unittest.main()
