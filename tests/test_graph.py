import pytest
from graph.business_graph import business_graph


@pytest.mark.asyncio
async def test_business_graph_basic_queries():
    result = await business_graph.ainvoke({
        "question": "Find the customer details for Ravi Kumar."
    })
    assert result is not None
    assert "response" in result
