from typing import TypedDict, List


class BusinessState(TypedDict):

    question: str
    category: str
    
    requirements: List[str]
    customer_name: str

    customer_data: str
    complaint_data: str
    policy_context: str

    decision: str
    ticket_result: str
    response: str
