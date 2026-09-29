import pytest
from backend.langchain_service import generate_langchain_response


@pytest.mark.asyncio
async def test_langchain_service():
    response = await generate_langchain_response("What is the role of an AI Business Assistant?")
    assert response is not None
    assert len(response) > 0
