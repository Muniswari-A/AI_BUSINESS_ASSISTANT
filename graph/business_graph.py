from langgraph.graph import (
    StateGraph,
    START,
    END
)

from graph.state import BusinessState

from graph.nodes import (
    understand_request_node,
    retrieve_information_node,
    business_analysis_node,
    action_node,
    final_response_node
)


def route_decision(state: BusinessState):
    decision = state.get("decision", "")
    
    if decision == "CREATE_TICKET":
        return "action"
    
    return "final_response"


def create_business_graph():
    graph = StateGraph(BusinessState)

    # Add Nodes
    graph.add_node("understand", understand_request_node)
    graph.add_node("retrieve", retrieve_information_node)
    graph.add_node("analysis", business_analysis_node)
    graph.add_node("action", action_node)
    graph.add_node("final_response", final_response_node)

    # Initial routing
    graph.add_edge(START, "understand")
    graph.add_edge("understand", "retrieve")
    graph.add_edge("retrieve", "analysis")
    
    # Decision routing
    graph.add_conditional_edges(
        "analysis",
        route_decision,
        {
            "action": "action",
            "final_response": "final_response"
        }
    )
    
    # Ticket creation always goes to final response
    graph.add_edge("action", "final_response")
    
    # Final response goes to end
    graph.add_edge("final_response", END)

    return graph.compile()


business_graph = create_business_graph()
