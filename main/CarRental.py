from util.db_conn_util import DBConnUtil

# Provide the relative or absolute path to your properties file
conn = DBConnUtil.get_connection(r'C:\Users\anush\PycharmProjects\Car Rental System\util\db.properties')
#
# if conn:
#     print("✅ Database connection established!")
#     conn.close()
# else:
#     print("❌ Failed to connect to the database.")


from dao.lease_repo_impl import ICarLeaseRepositoryImpl
from entity.car import Vehicle
from entity.customer import Customer
from exception.car_not_found_exception import  CarNotFoundException
from exception.customer_not_found_exception import  CustomerrNotFoundException
from exception.lease_not_found_exception import  LeaseNotFoundException
from datetime import date


def main():
    repo = ICarLeaseRepositoryImpl()

    while True:
        print("\n===== Car Rental System Menu =====")
        print("1. Car Management")
        print("2. Customer Management")
        print("3. Lease Management")
        print("4. Payment Handling")
        print("5. Exit")
        category = input("Enter your choice: ")

        try:
            if category == "1":
                print("\n--- Car Management ---")
                print("1. Add Car")
                print("2. Remove Car")
                print("3. List Available Cars")
                print("4. List Rented Cars")
                print("5. Find Car by ID")
                sub_choice = input("Enter your choice: ")

                if sub_choice == "1":
                    make = input("Enter make: ")
                    model = input("Enter model: ")
                    year = int(input("Enter year: "))
                    rate = float(input("Enter daily rate: "))
                    status = "available"
                    passenger_capacity = int(input("Enter passenger capacity: "))
                    engine_capacity = float(input("Enter engine capacity: "))
                    car = Vehicle(None, make, model, year, rate, status, passenger_capacity, engine_capacity)
                    repo.addCar(car)
                    print("✅ Car added successfully.")

                elif sub_choice == "2":
                    car_id = int(input("Enter car ID to remove: "))
                    repo.removeCar(car_id)
                    print("✅ Car removed successfully.")

                elif sub_choice == "3":
                    cars = repo.listAvailableCars()
                    for car in cars:
                        print(car)

                elif sub_choice == "4":
                    cars = repo.listRentedCars()
                    for car in cars:
                        print(car)

                elif sub_choice == "5":
                    car_id = int(input("Enter car ID: "))
                    car = repo.findCarById(car_id)
                    print(car)

                else:
                    print("❌ Invalid choice.")

            elif category == "2":
                print("\n--- Customer Management ---")
                print("1. Add Customer")
                print("2. Remove Customer")
                print("3. List Customers")
                print("4. Find Customer by ID")
                print("5. Update Customer")
                sub_choice = input("Enter your choice: ")

                if sub_choice == "1":
                    first_name = input("Enter first name: ")
                    last_name = input("Enter last name: ")
                    email = input("Enter email: ")
                    phone = input("Enter phone number: ")
                    customer = Customer(None, first_name, last_name, email, phone)
                    repo.addCustomer(customer)
                    print("✅ Customer added successfully.")

                elif sub_choice == "2":
                    customer_id = int(input("Enter customer ID to remove: "))
                    repo.removeCustomer(customer_id)
                    print("✅ Customer removed successfully.")

                elif sub_choice == "3":
                    customers = repo.listCustomers()
                    for cust in customers:
                        print(cust)

                elif sub_choice == "4":
                    customer_id = int(input("Enter customer ID: "))
                    customer = repo.findCustomerById(customer_id)
                    print(customer)

                elif sub_choice == "5":
                    customer_id = int(input("Enter customer ID to update: "))
                    first_name = input("Enter new first name: ")
                    last_name = input("Enter new last name: ")
                    email = input("Enter new email: ")
                    phone = input("Enter new phone number: ")
                    customer = Customer(customer_id, first_name, last_name, email, phone)
                    repo.updateCustomer(customer)
                    print("✅ Customer information updated successfully.")

                else:
                    print("❌ Invalid choice.")

            elif category == "3":
                print("\n--- Lease Management ---")
                print("1. Create Lease")
                print("2. Return Car")
                print("3. List Active Leases")
                print("4. List Lease History")
                sub_choice = input("Enter your choice: ")

                if sub_choice == "1":
                    customer_id = int(input("Enter customer ID: "))
                    car_id = int(input("Enter car ID: "))
                    start_date = input("Enter lease start date (YYYY-MM-DD): ")
                    end_date = input("Enter lease end date (YYYY-MM-DD): ")
                    lease = repo.createLease(customer_id, car_id, date.fromisoformat(start_date), date.fromisoformat(end_date))
                    print("✅ Lease created successfully:", lease)

                elif sub_choice == "2":
                    lease_id = int(input("Enter lease ID to return car: "))
                    lease = repo.returnCar(lease_id)
                    print("✅ Car returned successfully:", lease)

                elif sub_choice == "3":
                    leases = repo.listActiveLeases()
                    for lease in leases:
                        print(lease)

                elif sub_choice == "4":
                    leases = repo.listLeaseHistory()
                    for lease in leases:
                        print(lease)

                else:
                    print("❌ Invalid choice.")

            elif category == "4":
                print("\n--- Payment Handling ---")
                lease_id = int(input("Enter lease ID: "))
                amount = float(input("Enter payment amount: "))
                lease = repo.findLeaseById(lease_id)
                repo.recordPayment(lease, amount)
                print("✅ Payment recorded successfully.")

            elif category == "5":
                print("Exiting... Goodbye!")
                break

            else:
                print("❌ Invalid category. Please try again.")

        except CarNotFoundException as e:
            print(f"❌ Error: {e}")

        except CustomerrNotFoundException as e:
            print(f"❌ Error: {e}")

        except LeaseNotFoundException as e:
            print(f"❌ Error: {e}")

        except Exception as e:
            print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()


