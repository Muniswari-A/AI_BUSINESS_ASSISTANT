import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "business.db")

def get_connection():
    # Use check_same_thread=False since MCP/FastAPI might query from different async threads
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    # Row factory allows us to access columns by name like a dictionary
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Create Customers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    
    # 2. Create Complaints Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            issue TEXT NOT NULL
        )
    """)
    
    # 3. Create Tickets Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            customer_name TEXT NOT NULL,
            issue TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    
    # Seed initial test data ONLY if the database is brand new
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        customers = [
            ("C001", "Ravi Kumar", "ravi@example.com", "Active"),
            ("C002", "Priya", "priya@example.com", "Inactive"),
            ("C003", "Arun", "arun@example.com", "Active")
        ]
        cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?)", customers)
        
        complaints = [
            ("Ravi Kumar", "Damaged product received on last order."),
            ("Priya", "Billing issue: overcharged for subscription.")
        ]
        cursor.executemany("INSERT INTO complaints (customer_name, issue) VALUES (?, ?)", complaints)
        
    conn.commit()
    conn.close()

# Automatically initialize database when this module is loaded
init_db()
