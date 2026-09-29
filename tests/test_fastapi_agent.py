import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    print("\n" + "="*50)
    print("Testing GET /health")
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    print("Health response:", data)
    assert "status" in data
    assert "ollama" in data


@pytest.mark.parametrize("name, message", [
    ("Customer request", "Find the customer details for Ravi Kumar."),
    ("Policy request", "How many days do customers have to request a refund?"),
    ("Combined request", "Ravi Kumar has a damaged product. Check his complaint against the refund policy."),
    ("Ticket request", "Ravi Kumar has a damaged product. Create a support ticket if required."),
    ("Missing customer", "Create a support ticket for a damaged product."),
    ("General question", "What is Artificial Intelligence?"),
    ("Unknown customer", "Find the customer details for John Smith.")
])
def test_assistant_endpoint(name: str, message: str):
    print("\n" + "="*50)
    print(f"Testing POST /api/assistant: {name}")
    print(f"Message: {message}")
    print("-" * 50)
    response = client.post("/api/assistant", json={"message": message})
    
    assert response.status_code == 200, f"Error {response.status_code}: {response.text}"
    data = response.json()
    
    print(f"Decision: {data.get('decision')}")
    print(f"Ticket: {data.get('ticket')}")
    print(f"Response:\n{data.get('response')}")
    
    assert "response" in data
    assert "message" in data
