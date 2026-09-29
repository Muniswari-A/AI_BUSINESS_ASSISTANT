from langchain_core.tools import tool

@tool
def search_customer(customer_name: str) -> str:
    """
    Search for a customer by their name.
    
    Args:
        customer_name: The name of the customer to search for.
        
    Returns:
        The customer's details as a string if found, otherwise "Customer not found."
    """
    # A small hardcoded dictionary of customers
    customers = {
        "Ravi Kumar": {
            "customer_id": "C001",
            "name": "Ravi Kumar",
            "email": "ravi.kumar@example.com",
            "status": "Active"
        },
        "Priya": {
            "customer_id": "C002",
            "name": "Priya",
            "email": "priya@example.com",
            "status": "Inactive"
        },
        "Arun": {
            "customer_id": "C003",
            "name": "Arun",
            "email": "arun@example.com",
            "status": "Active"
        }
    }
    
    # Check if the customer exists in our dictionary
    if customer_name in customers:
        customer = customers[customer_name]
        # Return the customer details formatted as a string
        return (
            f"Customer ID: {customer['customer_id']}, "
            f"Name: {customer['name']}, "
            f"Email: {customer['email']}, "
            f"Status: {customer['status']}"
        )
    else:
        return "Customer not found."
