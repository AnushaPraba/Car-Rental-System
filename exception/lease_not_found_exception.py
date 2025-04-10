class LeaseNotFoundException(Exception):
    def __init__(self, message="Lease with the given ID was not found."):
        super().__init__(message)