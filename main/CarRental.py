from dao.lease_repo_impl import ICarLeaseRepositoryImpl
from entity.car import Vehicle
from entity.customer import Customer
from exception.car_not_found_exception import  CarNotFoundException
from exception.customer_not_found_exception import  CustomerrNotFoundException
from exception.lease_not_found_exception import  LeaseNotFoundException
from exception.invalid_customer_detail_exception import DuplicateCustomerException, DuplicateUserNameException, \
    InvalidPasswordException
from exception.invalid_customer_detail_exception import InvalidEmailException
from exception.invalid_customer_detail_exception import InvalidPhoneNumberException
from util.validation import validate_email, validate_phone,validate_password,hash_password
from dao.user_manager import UserManager
from datetime import date
from tabulate import tabulate


def main():
    user_manager = UserManager()

    while True:
        print("1. Sign Up")
        print("2. Log In")
        choice = input("Enter your choice: ")

        if choice == "1":
            user_manager.signup_customer()
        elif choice == "2":
            role,customerID=user_manager.login()
            if role=="admin":
                admin_menu()
            elif role=="customer":
                customer_menu(customerID)
        else:
            print("Invalid choice, please try again.")

def admin_menu():
    repo = ICarLeaseRepositoryImpl()

    while True:
        print("\n===== Admin Menu =====")
        print("1. Add Car")
        print("2. Remove Car")
        print("3. List Available Cars")
        print("4. List Rented Cars")
        print("5. Find Car by ID")
        print("6. Add Customer")
        print("7. Remove Customer")
        print("8. Update Customer")
        print("9. List Customers")
        print("10. Find Customer by ID")
        print("11. List Active Leases")
        print("12. List Lease History")
        print("13. Record Payment")
        print("14. View Payment History")
        print("15. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                make = input("Enter make: ")
                model = input("Enter model: ")
                year = int(input("Enter year: "))
                rate = float(input("Enter daily rate: "))
                status = "available"
                passenger_capacity = int(input("Enter passenger capacity: "))
                engine_capacity = float(input("Enter engine capacity(in litres): "))
                car = Vehicle(None, make, model, year, rate, status, passenger_capacity, engine_capacity)
                repo.addCar(car)
                print("Car added successfully.")

            except Exception as e:
                print(f"{e}")

        elif choice == "2":
            try:
                car_id = int(input("Enter car ID to remove: "))
                repo.removeCar(car_id)
                print("Car removed successfully.")

            except CarNotFoundException as e:
                print(f"{e}")

            except Exception as e:
                print(f"{e}")

        elif choice == "3":
            try:
                cars = repo.listAvailableCars()
                if cars:
                    headers = [
                                "Vehicle ID","Make", "Model", "Year", "Rate",
                                "Status", "Passenger Capacity", "Engine Capacity"
                            ]
                    print(tabulate(cars, headers=headers, tablefmt="fancy_grid"))
                else:
                    print("No available cars found.")

            except CarNotFoundException as e:
                print(f"{e}")

            except Exception as e:
                print(f"{e}")

        elif choice == "4":
            try:
                cars = repo.listRentedCars()
                if cars:
                    headers = [
                            "Vehicle ID", "Make", "Model", "Year", "Rate",
                            "Status", "Passenger Capacity", "Engine Capacity"
                        ]
                    print(tabulate(cars, headers=headers, tablefmt="fancy_grid"))
                else:
                    print("No rented cars found.")

            except CarNotFoundException as e:
                print(f"{e}")

            except Exception as e:
                print(f"{e}")

        elif choice == "5":
            try:
                car_id = int(input("Enter car ID: "))
                car = repo.findCarById(car_id)
                print(car)

            except CarNotFoundException as e:
                print(f"{e}")

            except Exception as e:
                print(f"{e}")

        elif choice == "6":
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            while True:
                email = input("Enter Email: ")
                try:
                    if validate_email(email):
                        break
                except InvalidEmailException as e:
                    print(e)

            while True:
                phone = input("Enter Phone Number: ")
                try:
                    if validate_phone(phone):
                        break
                except InvalidPhoneNumberException as e:
                        print(e)

            if repo.isEmailOrPhoneExists(email, phone):
                raise DuplicateCustomerException("Another Customer with email_id or phone_number already exists.")

            while True:
                username = input("Choose a Username: ")
                try:
                    if repo.is_username_unique( username):
                        break
                except DuplicateUserNameException as e:
                    print(e)

            while True:
                password = input("Choose a Password: ")
                try:
                    if validate_password(password):
                        hashed_password = hash_password(password)
                        break
                except InvalidPasswordException as e:
                    print(e)

            customer = Customer(None, first_name, last_name, email, phone)
            customer_id=repo.addCustomer(customer)

            repo.addUser(username, hashed_password, 'customer', customer_id)

            print("Customer added successfully with login credentials.")

        elif choice == "7":
            try:
                customer_id = int(input("Enter customer ID to remove: "))
                repo.removeCustomer(customer_id)
                print("Customer removed successfully.")
            except CustomerrNotFoundException as e:
                print(f"{e}")
            except Exception as e:
                print(f"{e}")

        elif choice == "8":
            try:
                customer_id = int(input("Enter customer ID to update: "))
                existing_customer = repo.findCustomerById(customer_id)

                print("Enter new details (leave blank to keep current value):")
                first_name = input(
                    f"First name [{existing_customer.get_firstName()}]: ") or existing_customer.get_firstName()
                last_name = input(
                    f"Last name [{existing_customer.get_lastName()}]: ") or existing_customer.get_lastName()
                email = input(f"Email [{existing_customer.get_email()}]: ") or existing_customer.get_email()
                phone = input(f"Phone [{existing_customer.get_phoneNumber()}]: ") or existing_customer.get_phoneNumber()

                validate_email(email)
                validate_phone(phone)

                if repo.isEmailOrPhoneExists(email, phone, customer_id):
                    raise DuplicateCustomerException("Another customer with this email or phone number already exists.")

                updated_customer = Customer(customer_id, first_name, last_name, email, phone)
                repo.updateCustomer(updated_customer)
                print("Customer updated successfully.")

            except CustomerrNotFoundException as e:
                print(f"{e}")
            except DuplicateCustomerException as e:
                print(f"{e}")
            except InvalidEmailException as e:
                print(f"{e}")
            except InvalidPhoneNumberException as e:
                print(f"{e}")
            except Exception as e:
                print(f"{e}")

        elif choice == "9":
            try:
                customers = repo.listCustomers()
                if customers:
                    headers = ["Customer ID", "First Name", "Last Name", "Email", "Phone Number"]
                    print(tabulate(customers, headers=headers, tablefmt="fancy_grid"))
                else:
                    print("No customers found.")
            except Exception as e:
                print(f"{e}")

        elif choice == "10":
            try:
                customer_id = int(input("Enter customer ID: "))
                customer = repo.findCustomerById(customer_id)
                print(customer)
            except CustomerrNotFoundException as e:
                print(f"{e}")
            except Exception as e:
                print(f"{e}")

        elif choice == "11":
            try:
                leases = repo.listActiveLeases()
                if leases:
                    headers = ["Lease ID", "Cust ID", "Customer Name", "Phone","Vehicle ID", "Model", "Rate","Start Date", "End Date", "Days", "Expected Amount", "Payment Status"]
                    print(tabulate(leases, headers=headers, tablefmt="fancy_grid"))
                else:
                    print("No lease records found.")
            except Exception as e:
                print(f"{e}")

        elif choice == "12":
            try:
                leases = repo.listLeaseHistory()
                if leases:
                    headers = ["Lease ID", "Cust ID", "Customer Name", "Phone","Vehicle ID", "Model", "Rate","Start Date", "End Date", "Days", "Expected Amount", "Payment Status"]
                    print(tabulate(leases, headers=headers, tablefmt="fancy_grid"))
                else:
                    print("No lease records found.")
            except Exception as e:
                print(f"{e}")

        elif choice == '13':
            try:
                leaseID = int(input("Lease ID: "))
                lease = repo.findLeaseById(leaseID)
                amount = float(input("Amount: "))
                repo.recordPayment(lease, amount)
                print("Payment recorded.")
            except LeaseNotFoundException as e:
                print(f"{e}")
            except Exception as e:
                print(f"{e}")

        elif choice == "14":
            try:
                history = repo.get_payment_history()
                if history:
                    headers = ["Payment ID", "Lease ID", "Vehicle ID","Customer ID","Customer Name", "Payment Date ", "Amount",
                               "Expected Amount", "Payment Status"]
                    print(tabulate(history, headers=headers, tablefmt="fancy_grid"))
                else:
                    print("No payment records found.")

            except Exception as e:
                print(f"{e}")

        elif choice == "15":
            print("Logged out")
            break

        else:
            print("Invalid choice. Please try again.")

def customer_menu(customerID):
    repo = ICarLeaseRepositoryImpl()

    while True:
        print("\n===== Customer Menu =====")
        print("1. List Available Cars")
        print("2. Create Lease")
        print("3. Return Car")
        print("4. View My Lease History")
        print("5. Make Payment")
        print("6. View My Payments")
        print("7. Logout")

        choice = input("Enter choice: ")

        try:
            if choice == "1":
                cars = repo.listAvailableCars()
                if cars:
                    headers = [
                        "Vehicle ID", "Make", "Model", "Year", "Rate",
                        "Status", "Passenger Capacity", "Engine Capacity"
                    ]
                    print(tabulate(cars, headers=headers, tablefmt="fancy_grid"))
                else:
                    print("No available cars found.")

            elif choice == "2":
                car_id = int(input("Enter car ID: "))
                start_date = input("Enter lease start date (YYYY-MM-DD): ")
                end_date = input("Enter lease end date (YYYY-MM-DD): ")
                lease = repo.createLease(customerID, car_id, date.fromisoformat(start_date), date.fromisoformat(end_date))
                print("Lease created successfully:", lease)

            elif choice == "3":
                lease_id = int(input("Enter lease ID to return car: "))
                lease = repo.returnCar(lease_id)
                print("Car returned successfully:", lease)

            elif choice == "4":
                leases = repo.listLeasesByCustomer(customerID)
                if leases:
                    headers = ["Lease ID","Vehicle ID", "Model", "Rate","Start Date", "End Date", "Days", "Expected Amount","Payment Status"]
                    print(tabulate(leases, headers=headers, tablefmt="fancy_grid"))
                else:
                    print("No lease records found.")

            elif choice == "5":
                leaseID = int(input("Lease ID: "))
                lease = repo.findLeaseById(leaseID)
                if lease is None:
                    print("Lease not found.")
                elif lease.get_customerID()!= customerID:
                    print("You are not authorized to make payment for this lease.")
                else:
                    amount = float(input("Amount: "))
                    repo.recordPayment(lease, amount)
                    print("Payment recorded.")

            elif choice == "6":
                history=repo.get_payment_history_by_customer(customerID)
                if history:
                    headers = ["Payment ID", "Lease ID", "Vehicle ID", "Payment Date ","Amount", "Expected Amount","Payment Status"]
                    print(tabulate(history, headers=headers, tablefmt="fancy_grid"))
                else:
                    print("No payment records found.")

            elif choice == "7":
                print("Logged out")
                break

            else:
                print("Invalid choice.")

        except CarNotFoundException as e:
            print(f"{e}")

        except CustomerrNotFoundException as e:
            print(f"{e}")

        except LeaseNotFoundException as e:
            print(f"{e}")

        except InvalidEmailException as e:
            print(f"{e}")

        except InvalidPhoneNumberException as e:
            print(f"{e}")

        except DuplicateCustomerException as e:
            print(f"{e}")

        except ValueError as e:
            print(f"{e}")

        except Exception as e:
            print(f"{e}")

if __name__ == "__main__":
    main()


