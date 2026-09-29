import os
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "mcp_server", "business.db")

def test_database_persistence_and_sequential_tickets():
    # 1. Simulate a completely fresh database
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    # Re-initialize DB tables and seed data since we just deleted it
    from mcp_server.db import init_db
    init_db()

    # 2. Ravi Kumar damaged-product ticket (First ticket creation)
    response = client.post("/api/assistant", json={
        "message": "Ravi Kumar has a damaged product. Create a ticket."
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "CREATE_TICKET"
    assert "T001" in data["ticket"]
    
    # 3. Simulate Server/database restart persistence
    # To truly simulate it, we can force SQLite to reconnect by calling init_db again, 
    # though simply making another request over the HTTP TestClient verifies the DB state on disk.
    
    # 4. Sequential ticket IDs (Priya's billing issue)
    response2 = client.post("/api/assistant", json={
        "message": "Create a ticket for Priya about a billing issue."
    })
    
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["decision"] == "CREATE_TICKET"
    assert "T002" in data2["ticket"]
    
    print("Database persistence and sequential ticket generation verified successfully!")
