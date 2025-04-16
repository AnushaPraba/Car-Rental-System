import sys
import os
from dao.lease_repo_impl import ICarLeaseRepositoryImpl
from entity.car import Vehicle
from entity.customer import Customer
from exception.car_not_found_exception import CarNotFoundException
from exception.customer_not_found_exception import CustomerNotFoundException
from exception.lease_not_found_exception import LeaseNotFoundException
from exception.invalid_customer_detail_exception import (
    DuplicateCustomerException, DuplicateUserNameException,
    InvalidPasswordException, InvalidEmailException, InvalidPhoneNumberException
)
from util.validation import validate_email, validate_phone, validate_password, hash_password
from dao.user_manager import UserManager
from datetime import date
from tabulate import tabulate

# Ensure the project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main():
    user_manager = UserManager()

    while True:
        print("\n===== Main Menu =====")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            user_manager.signup_customer()
        elif choice == "2":
            role, customer_id = user_manager.login()
            if role == "admin":
                admin_menu()
            elif role == "customer":
                customer_menu(customer_id)
        elif choice == "3":
            print("Exiting the system. Goodbye!")
            break
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

        try:
            if choice == "1":
                add_car(repo)
            elif choice == "2":
                remove_car(repo)
            elif choice == "3":
                list_available_cars(repo)
            elif choice == "4":
                list_rented_cars(repo)
            elif choice == "5":
                find_car_by_id(repo)
            elif choice == "6":
                add_customer(repo)
            elif choice == "7":
                remove_customer(repo)
            elif choice == "8":
                update_customer(repo)
            elif choice == "9":
                list_customers(repo)
            elif choice == "10":
                find_customer_by_id(repo)
            elif choice == "11":
                list_active_leases(repo)
            elif choice == "12":
                list_lease_history(repo)
            elif choice == "13":
                record_payment(repo)
            elif choice == "14":
                view_payment_history(repo)
            elif choice == "15":
                print("Logged out")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}")


def customer_menu(customer_id):
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
                list_available_cars(repo)
            elif choice == "2":
                create_lease(repo, customer_id)
            elif choice == "3":
                return_car(repo)
            elif choice == "4":
                view_lease_history(repo, customer_id)
            elif choice == "5":
                make_payment(repo, customer_id)
            elif choice == "6":
                view_customer_payments(repo, customer_id)
            elif choice == "7":
                print("Logged out")
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"Error: {e}")


# --- Admin Functions ---
def add_car(repo):
    make = input("Enter make: ")
    model = input("Enter model: ")
    year = int(input("Enter year: "))
    rate = float(input("Enter daily rate: "))
    status = "available"
    passenger_capacity = int(input("Enter passenger capacity: "))
    engine_capacity = float(input("Enter engine capacity (in litres): "))
    car = Vehicle(None, make, model, year, rate, status, passenger_capacity, engine_capacity)
    repo.addCar(car)
    print("Car added successfully.")


def remove_car(repo):
    car_id = int(input("Enter car ID to remove: "))
    repo.removeCar(car_id)
    print("Car removed successfully.")


def list_available_cars(repo):
    cars = repo.listAvailableCars()
    if cars:
        headers = ["Vehicle ID", "Make", "Model", "Year", "Rate", "Status", "Passenger Capacity", "Engine Capacity"]
        print(tabulate(cars, headers=headers, tablefmt="fancy_grid"))
    else:
        print("No available cars found.")


def list_rented_cars(repo):
    cars = repo.listRentedCars()
    if cars:
        headers = ["Vehicle ID", "Make", "Model", "Year", "Rate", "Status", "Passenger Capacity", "Engine Capacity"]
        print(tabulate(cars, headers=headers, tablefmt="fancy_grid"))
    else:
        print("No rented cars found.")


def find_car_by_id(repo):
    car_id = int(input("Enter car ID: "))
    car = repo.findCarById(car_id)
    print(car)


def add_customer(repo):
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = get_valid_input("Enter Email: ", validate_email, InvalidEmailException)
    phone = get_valid_input("Enter Phone Number: ", validate_phone, InvalidPhoneNumberException)

    if repo.isEmailOrPhoneExists(email, phone):
        raise DuplicateCustomerException("Another customer with this email or phone number already exists.")

    username = get_valid_input("Choose a Username: ", repo.is_username_unique, DuplicateUserNameException)
    password = get_valid_input("Choose a Password: ", validate_password, InvalidPasswordException)
    hashed_password = hash_password(password)

    customer = Customer(None, first_name, last_name, email, phone)
    customer_id = repo.addCustomer(customer)
    repo.addUser(username, hashed_password, 'customer', customer_id)
    print("Customer added successfully with login credentials.")


def remove_customer(repo):
    customer_id = int(input("Enter customer ID to remove: "))
    repo.removeCustomer(customer_id)
    print("Customer removed successfully.")


def update_customer(repo):
    customer_id = int(input("Enter customer ID to update: "))
    existing_customer = repo.findCustomerById(customer_id)

    print("Enter new details (leave blank to keep current value):")
    first_name = input(f"First name [{existing_customer.get_firstName()}]: ") or existing_customer.get_firstName()
    last_name = input(f"Last name [{existing_customer.get_lastName()}]: ") or existing_customer.get_lastName()
    email = input(f"Email [{existing_customer.get_email()}]: ") or existing_customer.get_email()
    phone = input(f"Phone [{existing_customer.get_phoneNumber()}]: ") or existing_customer.get_phoneNumber()

    validate_email(email)
    validate_phone(phone)

    if repo.isEmailOrPhoneExists(email, phone, customer_id):
        raise DuplicateCustomerException("Another customer with this email or phone number already exists.")

    updated_customer = Customer(customer_id, first_name, last_name, email, phone)
    repo.updateCustomer(updated_customer)
    print("Customer updated successfully.")


def list_customers(repo):
    customers = repo.listCustomers()
    if customers:
        headers = ["Customer ID", "First Name", "Last Name", "Email", "Phone Number"]
        print(tabulate(customers, headers=headers, tablefmt="fancy_grid"))
    else:
        print("No customers found.")


def find_customer_by_id(repo):
    customer_id = int(input("Enter customer ID: "))
    customer = repo.findCustomerById(customer_id)
    print(customer)


def list_active_leases(repo):
    leases = repo.listActiveLeases()
    if leases:
        headers = ["Lease ID", "Cust ID", "Customer Name", "Phone", "Vehicle ID", "Model", "Rate", "Start Date",
                   "End Date", "Days", "Expected Amount", "Payment Status"]
        print(tabulate(leases, headers=headers, tablefmt="fancy_grid"))
    else:
        print("No active leases found.")


def list_lease_history(repo):
    leases = repo.listLeaseHistory()
    if leases:
        headers = ["Lease ID", "Cust ID", "Customer Name", "Phone", "Vehicle ID", "Model", "Rate", "Start Date",
                   "End Date", "Days", "Expected Amount", "Payment Status"]
        print(tabulate(leases, headers=headers, tablefmt="fancy_grid"))
    else:
        print("No lease history found.")


def record_payment(repo):
    lease_id = int(input("Lease ID: "))
    lease = repo.findLeaseById(lease_id)
    amount = float(input("Amount: "))
    repo.recordPayment(lease, amount)
    print("Payment recorded successfully.")


def view_payment_history(repo):
    history = repo.get_payment_history()
    if history:
        headers = ["Payment ID", "Lease ID", "Vehicle ID", "Customer ID", "Customer Name", "Payment Date", "Amount",
                   "Expected Amount", "Payment Status"]
        print(tabulate(history, headers=headers, tablefmt="fancy_grid"))
    else:
        print("No payment history found.")


# --- Customer Functions ---
def create_lease(repo, customer_id):
    car_id = int(input("Enter car ID: "))
    start_date = input("Enter lease start date (YYYY-MM-DD): ")
    end_date = input("Enter lease end date (YYYY-MM-DD): ")
    lease = repo.createLease(customer_id, car_id, date.fromisoformat(start_date), date.fromisoformat(end_date))
    print("Lease created successfully:", lease)


def return_car(repo):
    lease_id = int(input("Enter lease ID to return car: "))
    lease = repo.returnCar(lease_id)
    print("Car returned successfully:", lease)


def view_lease_history(repo, customer_id):
    leases = repo.listLeasesByCustomer(customer_id)
    if leases:
        headers = ["Lease ID", "Vehicle ID", "Model", "Rate", "Start Date", "End Date", "Days", "Expected Amount",
                   "Payment Status"]
        print(tabulate(leases, headers=headers, tablefmt="fancy_grid"))
    else:
        print("No lease history found.")


def make_payment(repo, customer_id):
    lease_id = int(input("Lease ID: "))
    lease = repo.findLeaseById(lease_id)
    if lease.get_customerID() != customer_id:
        print("You are not authorized to make payment for this lease.")
        return
    amount = float(input("Amount: "))
    repo.recordPayment(lease, amount)
    print("Payment recorded successfully.")


def view_customer_payments(repo, customer_id):
    history = repo.get_payment_history_by_customer(customer_id)
    if history:
        headers = ["Payment ID", "Lease ID", "Vehicle ID", "Payment Date", "Amount", "Expected Amount",
                   "Payment Status"]
        print(tabulate(history, headers=headers, tablefmt="fancy_grid"))
    else:
        print("No payment history found.")


# --- Utility Functions ---
def get_valid_input(prompt, validation_func, exception_class):
    while True:
        value = input(prompt)
        try:
            if validation_func(value):
                return value
        except exception_class as e:
            print(e)


if __name__ == "__main__":
    main()


