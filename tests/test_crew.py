import pytest
from agents.business_crew import run_business_crew


@pytest.mark.slow
def test_business_crew():
    request = """
    Ravi Kumar has a damaged product.
    Analyze the customer request and identify what business action should be taken.
    """
    result = run_business_crew(request)
    assert result is not None
