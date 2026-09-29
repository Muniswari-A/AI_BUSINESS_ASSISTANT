from mcp_server.client import get_mcp_client


async def list_mcp_tools():

    async with get_mcp_client() as client:

        result = await client.list_tools()

        return [
            tool.name
            for tool in result.tools
        ]


async def call_mcp_tool(
    tool_name: str,
    arguments: dict
):

    async with get_mcp_client() as client:

        result = await client.call_tool(
            tool_name,
            arguments=arguments
        )

        if result.isError:
            return "MCP tool execution failed."

        texts = []

        for content in result.content:

            if hasattr(content, "text"):
                texts.append(content.text)

        return "\n".join(texts)
