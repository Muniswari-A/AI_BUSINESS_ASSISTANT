import pytest
from agents.langchain_agent import run_customer_agent


@pytest.mark.asyncio
async def test_customer_agent():
    response = await run_customer_agent("Find the customer details for Ravi Kumar.")
    assert response is not None
    assert len(response) > 0
