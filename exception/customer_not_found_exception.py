class CustomerrNotFoundException(Exception):
    def __init__(self, message="Customer with the given ID was not found."):
        super().__init__(message)