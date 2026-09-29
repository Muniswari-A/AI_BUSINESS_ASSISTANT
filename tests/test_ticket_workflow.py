import pytest
from graph.business_graph import business_graph


@pytest.mark.asyncio
async def test_ticket_workflow_scenarios():
    result = await business_graph.ainvoke({
        "question": "Ravi Kumar has a damaged product. Check his complaint and create a support ticket if required."
    })
    assert result is not None
    assert "decision" in result
