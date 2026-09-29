from agents.tools import search_customer


def test_search_customer_tool():
    result_known = search_customer.invoke({"customer_name": "Ravi Kumar"})
    assert "C001" in result_known or "Ravi Kumar" in result_known

    result_unknown = search_customer.invoke({"customer_name": "Unknown Customer"})
    assert "not found" in result_unknown.lower()
