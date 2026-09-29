import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server.fastmcp import FastMCP
from mcp_server.db import get_connection
# Initialize the MCP server
mcp = FastMCP("DCI Business MCP Server")

@mcp.tool()
def search_customer(customer_name: str) -> str:
    """
    Search customer data in the database.
    
    Args:
        customer_name: The name of the customer to search for.
        
    Returns:
        Customer details (customer_id, name, email, status) if found, otherwise a not found message.
    """
    conn = get_connection()
    cursor = conn.cursor()
    clean_name = customer_name.strip(". ")
    cursor.execute("SELECT * FROM customers WHERE name LIKE ?", (f"%{clean_name}%",))
    customer = cursor.fetchone()
    conn.close()

    if customer:
        return f"Customer Found: ID: {customer['customer_id']}, Name: {customer['name']}, Email: {customer['email']}, Status: {customer['status']}"
    return "Customer not found."


@mcp.tool()
def search_complaint(customer_name: str) -> str:
    """
    Search complaint data in the database.
    
    Args:
        customer_name: The name of the customer whose complaint to search.
        
    Returns:
        Complaint details if found, otherwise "Complaint not found."
    """
    conn = get_connection()
    cursor = conn.cursor()
    clean_name = customer_name.strip(". ")
    cursor.execute("SELECT issue FROM complaints WHERE customer_name LIKE ?", (f"%{clean_name}%",))
    complaint = cursor.fetchone()
    conn.close()

    if complaint:
        return f"Complaint for {customer_name}: {complaint['issue']}"
    return "Complaint not found."


@mcp.tool()
def create_ticket(customer_name: str, issue: str) -> str:
    """
    Create a simple support ticket for a customer and save it to the database.
    
    Args:
        customer_name: The name of the customer creating the ticket.
        issue: A description of the issue.
        
    Returns:
        The generated ticket ID and status.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Generate a sequential ticket ID like T001, T002, etc. based on DB rows
    cursor.execute("SELECT COUNT(*) FROM tickets")
    count = cursor.fetchone()[0]
    ticket_id = f"T{count + 1:03d}"
    
    cursor.execute(
        "INSERT INTO tickets (ticket_id, customer_name, issue, status) VALUES (?, ?, ?, ?)",
        (ticket_id, customer_name, issue, "Open")
    )
    conn.commit()
    conn.close()
    
    return f"Ticket {ticket_id} created successfully. Status: Open"


if __name__ == "__main__":
    mcp.run()
