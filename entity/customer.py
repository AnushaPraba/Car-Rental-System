class Customer:
    def __init__(self, customerID=None, firstName=None, lastName=None, email=None, phoneNumber=None):
        self.__customerID = customerID
        self.__firstName = firstName
        self.__lastName = lastName
        self.__email = email
        self.__phoneNumber = phoneNumber

    def get_customerID(self):
        return self.__customerID

    def get_firstName(self):
        return self.__firstName

    def get_lastName(self):
        return self.__lastName

    def get_email(self):
        return self.__email

    def get_phoneNumber(self):
        return self.__phoneNumber

    def set_customerID(self, customerID):
        self.__customerID = customerID

    def set_firstName(self, firstName):
        self.__firstName = firstName

    def set_lastName(self, lastName):
        self.__lastName = lastName

    def set_email(self, email):
        self.__email = email

    def set_phoneNumber(self, phoneNumber):
        self.__phoneNumber = phoneNumber

    def __str__(self):
        return f"Customer[ID={self.get_customerID()}, Name={self.get_firstName()} {self.get_lastName()}, Email={self.get_email()}, Phone={self.get_phoneNumber()}]"

