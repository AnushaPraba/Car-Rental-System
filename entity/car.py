class Vehicle:
    def __init__(self, vehicleID=None, make=None, model=None, year=None, dailyRate=None, status=None, passengerCapacity=None, engineCapacity=None):
        self.__vehicleID = vehicleID
        self.__make = make
        self.__model = model
        self.__year = year
        self.__dailyRate = dailyRate
        self.__status = status
        self.__passengerCapacity = passengerCapacity
        self.__engineCapacity = engineCapacity

    # Getters and setters
    def get_vehicleID(self):
        return self.__vehicleID

    def get_make(self):
        return self.__make

    def get_model(self):
        return self.__model

    def get_year(self):
        return self.__year

    def get_dailyRate(self):
        return self.__dailyRate

    def get_status(self):
        return self.__status

    def get_passengerCapacity(self):
        return self.__passengerCapacity

    def get_engineCapacity(self):
        return self.__engineCapacity

    def set_vehicleID(self, vehicleID):
        self.__vehicleID = vehicleID

    def set_make(self, make):
        self.__make = make

    def set_model(self, model):
        self.__model = model

    def set_year(self, year):
        self.__year = year

    def set_dailyRate(self, dailyRate):
        self.__dailyRate = dailyRate

    def set_status(self, status):
        self.__status = status

    def set_passengerCapacity(self, passengerCapacity):
        self.__passengerCapacity = passengerCapacity

    def set_engineCapacity(self, engineCapacity):
        self.__engineCapacity = engineCapacity

    def __str__(self):
        return (f"Vehicle[ID={self.__vehicleID}, Make={self.__make}, Model={self.__model}, "
                f"Year={self.__year}, Rate={self.__dailyRate}, Status={self.__status}, "
                f"Passengers={self.__passengerCapacity}, Engine={self.__engineCapacity}L]")
