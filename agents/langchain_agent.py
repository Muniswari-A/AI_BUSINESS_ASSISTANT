from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage

from backend.config import OLLAMA_MODEL, OLLAMA_BASE_URL
from agents.tools import search_customer

# 1. Create the ChatOllama model
llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL
)

# 2. Bind the search_customer tool to the model
llm_with_tools = llm.bind_tools([search_customer])

async def run_customer_agent(message: str) -> str:
    """
    A simple async agent that can look up customer details.
    """
    # 3. Prepare the conversation history
    messages = [HumanMessage(content=message)]
    
    # 4. Send the user's message to the model
    ai_msg = await llm_with_tools.ainvoke(messages)
    
    # 5. Check if the model decided to call a tool
    if ai_msg.tool_calls:
        # Add the AI's tool request to our conversation history
        messages.append(ai_msg)
        
        # 6. Execute the requested tool(s)
        for tool_call in ai_msg.tool_calls:
            if tool_call["name"] == "search_customer":
                # Run our search_customer tool
                tool_output = search_customer.invoke(tool_call["args"])
                
                # Create a ToolMessage with the result
                tool_result_msg = ToolMessage(
                    content=str(tool_output),
                    tool_call_id=tool_call["id"]
                )
                
                # 7. Add the tool result to the conversation
                messages.append(tool_result_msg)
        
        # 8. Send the conversation back to the model so it can formulate a final answer
        final_ai_msg = await llm_with_tools.ainvoke(messages)
        
        # Return the final text response
        return final_ai_msg.content
        
    else:
        # 9. If no tool was needed, just return the AI's direct answer
        return ai_msg.content
