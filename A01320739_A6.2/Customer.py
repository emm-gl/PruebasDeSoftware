import os
import json

class CustomerManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def create_customer(self, customer_data):
        try:
            with open(self.file_path, 'a') as file:
                json.dump(customer_data, file)
                file.write('\n')  # separate entries by new line
            return True
        except Exception as e:
            print(f"Error creating customer: {e}")
            return False

    def delete_customer(self, customer_id):
        try:
            # Read all customers, filter out the one to be deleted, and rewrite the file without it
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
            with open(self.file_path, 'w') as file:
                for line in lines:
                    customer = json.loads(line)
                    if customer.get('id') != customer_id:
                        json.dump(customer, file)
                        file.write('\n')
            return True
        except Exception as e:
            print(f"Error deleting customer: {e}")
            return False

    def display_customer_info(self, customer_id):
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    customer = json.loads(line)
                    if customer.get('id') == customer_id:
                        return customer
            return None  # Customer not found
        except Exception as e:
            print(f"Error displaying customer information: {e}")
            return None

    def modify_customer_info(self, customer_id, new_data):
        try:
            # Read all customers, find the one to modify, update its data, and rewrite the file
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
            with open(self.file_path, 'w') as file:
                for line in lines:
                    customer = json.loads(line)
                    if customer.get('id') == customer_id:
                        customer.update(new_data)
                    json.dump(customer, file)
                    file.write('\n')
            return True
        except Exception as e:
            print(f"Error modifying customer information: {e}")
            return False

# Example usage:
if __name__ == "__main__":
    file_path = "customers.txt"
    manager = CustomerManager(file_path)

    # Create a customer
    customer_data = {"id": 1, "name": "John Doe", "email": "john@example.com"}
    manager.create_customer(customer_data)

    # Display customer information
    customer_info = manager.display_customer_info(1)
    print("Customer Information:")
    print(customer_info)

    # Modify customer information
    new_data = {"email": "john.doe@example.com"}
    manager.modify_customer_info(1, new_data)

    # Display modified customer information
    modified_info = manager.display_customer_info(1)
    print("Modified Customer Information:")
    print(modified_info)

    # Delete the customer
    manager.delete_customer(1)
