import pytest
from rag.rag_chain import answer_with_rag


@pytest.mark.asyncio
async def test_rag_chain_query():
    response = await answer_with_rag("How many days do customers have to request a refund?")
    assert response is not None
    assert len(response) > 0
