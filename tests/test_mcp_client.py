import pytest
from mcp_server.mcp_service import list_mcp_tools, call_mcp_tool


@pytest.mark.asyncio
async def test_mcp_tools_list_and_call():
    tools = await list_mcp_tools()
    assert "search_customer" in tools
    assert "search_complaint" in tools
    assert "create_ticket" in tools

    customer_res = await call_mcp_tool("search_customer", {"customer_name": "Ravi Kumar"})
    assert "Ravi Kumar" in customer_res or "Customer Found" in customer_res

    complaint_res = await call_mcp_tool("search_complaint", {"customer_name": "Ravi Kumar"})
    assert "Damaged product" in complaint_res or "Complaint" in complaint_res
