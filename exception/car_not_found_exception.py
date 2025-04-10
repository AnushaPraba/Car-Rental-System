class CarNotFoundException(Exception):
    def __init__(self, message="Car with the given ID was not found."):
        super().__init__(message)