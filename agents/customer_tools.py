from langchain_core.tools import tool

@tool
def search_customer(customer_name: str) -> str:
    """
    Search for a customer by their name and return their details.
    
    Args:
        customer_name (str): The name of the customer to search for.
        
    Returns:
        str: The customer's details if found, otherwise "Customer not found."
    """
    # Sample customer data
    customers = {
        "Ravi Kumar": {
            "customer_id": "C001",
            "email": "ravi@example.com",
            "status": "Active"
        },
        "Priya": {
            "customer_id": "C002",
            "email": "priya@example.com",
            "status": "Active"
        },
        "Arun": {
            "customer_id": "C003",
            "email": "arun@example.com",
            "status": "Inactive"
        }
    }
    
    # Check if the customer exists in our records
    if customer_name in customers:
        customer = customers[customer_name]
        return (
            f"Name: {customer_name}, "
            f"ID: {customer['customer_id']}, "
            f"Email: {customer['email']}, "
            f"Status: {customer['status']}"
        )
    else:
        return "Customer not found."
