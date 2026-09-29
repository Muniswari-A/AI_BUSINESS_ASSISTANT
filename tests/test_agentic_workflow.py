import pytest
import asyncio
from graph.business_graph import business_graph

@pytest.mark.asyncio
@pytest.mark.parametrize("name, question, expected_decision", [
    ("TEST 1 - Customer Lookup", "Find the customer details for Ravi Kumar.", "NO_ACTION"),
    ("TEST 2 - Complaint Lookup", "Check Ravi Kumar's complaint.", "NO_ACTION"),
    ("TEST 3 - Policy Question", "How many days do customers have to request a refund?", "NO_ACTION"),
    ("TEST 4 - Combined Business Analysis", "Ravi Kumar has a damaged product. Check his complaint against the refund policy.", "NO_ACTION"),
    ("TEST 5 - Missing Information", "Create a support ticket for a damaged product.", "MORE_INFORMATION_REQUIRED"),
    ("TEST 6 - General Question", "What is Artificial Intelligence?", "NO_ACTION"),
    ("TEST 7 - Unknown Customer", "Find the customer details for John Smith.", "NO_ACTION"),
])
async def test_agentic_workflow_scenarios(name, question, expected_decision):
    result = await business_graph.ainvoke({"question": question})
    
    decision = result.get("decision", "NO_ACTION")
    assert decision == expected_decision, f"Failed on {name}: expected {expected_decision}, got {decision}"
