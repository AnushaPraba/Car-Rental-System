class Lease:
    def __init__(self, leaseID=None, vehicleID=None, customerID=None, startDate=None, endDate=None, type=None,expectedAmount=None,paymentStatus=None):
        self.__leaseID = leaseID
        self.__vehicleID = vehicleID
        self.__customerID = customerID
        self.__startDate = startDate
        self.__endDate = endDate
        self.__type = type
        self.__expectedAmount=expectedAmount
        self.__paymentStatus=paymentStatus

    def get_leaseID(self):
        return self.__leaseID

    def get_vehicleID(self):
        return self.__vehicleID

    def get_customerID(self):
        return self.__customerID

    def get_startDate(self):
        return self.__startDate

    def get_endDate(self):
        return self.__endDate

    def get_type(self):
        return self.__type

    def get_expectedAmount(self):
        return self.__expectedAmount

    def get_paymentStatus(self):
        return self.__paymentStatus

    def set_leaseID(self, leaseID):
        self.__leaseID = leaseID

    def set_vehicleID(self, vehicleID):
        self.__vehicleID = vehicleID

    def set_customerID(self, customerID):
        self.__customerID = customerID

    def set_startDate(self, startDate):
        self.__startDate = startDate

    def set_endDate(self, endDate):
        self.__endDate = endDate

    def set_type(self, type):
        self.__type = type

    def set_expectedAmount(self,expectedAmount):
        self.__expectedAmount=expectedAmount

    def set_paymentStatus(self,paymentStatus):
        self.__paymentStatus=paymentStatus

    def __str__(self):
        return (
            f"Lease[ID={self.get_leaseID()}, VehicleID={self.get_vehicleID()}, CustomerID={self.get_customerID()}, "
            f"StartDate={self.get_startDate()}, EndDate={self.get_endDate()}, Type={self.get_type()}"
            f"ExpectedAmount={self.get_expectedAmount()},PaymentStatus={self.get_paymentStatus()}]"
        )
