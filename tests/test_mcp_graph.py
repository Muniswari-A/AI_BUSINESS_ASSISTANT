import pytest
from graph.business_graph import business_graph


@pytest.mark.asyncio
async def test_mcp_graph_integration():
    result = await business_graph.ainvoke({
        "question": "Ravi Kumar has a damaged product. Please check his customer details and complaint."
    })
    assert result is not None
    assert "customer_data" in result
    assert "complaint_data" in result
