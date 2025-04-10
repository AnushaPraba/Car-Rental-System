class Payment:
    def __init__(self, paymentID=None, leaseID=None, paymentDate=None, amount=None):
        self.__paymentID = paymentID
        self.__leaseID = leaseID
        self.__paymentDate = paymentDate
        self.__amount = amount

    def get_paymentID(self):
        return self.__paymentID

    def get_leaseID(self):
        return self.__leaseID

    def get_paymentDate(self):
        return self.__paymentDate

    def get_amount(self):
        return self.__amount

    def set_paymentID(self, paymentID):
        self.__paymentID = paymentID

    def set_leaseID(self, leaseID):
        self.__leaseID = leaseID

    def set_paymentDate(self, paymentDate):
        self.__paymentDate = paymentDate

    def set_amount(self, amount):
        self.__amount = amount
