import pytest
from graph.business_graph import business_graph


@pytest.mark.asyncio
async def test_mcp_rag_workflow():
    result = await business_graph.ainvoke({
        "question": "How many days do customers have to request a refund?"
    })
    assert result is not None
    assert "response" in result
