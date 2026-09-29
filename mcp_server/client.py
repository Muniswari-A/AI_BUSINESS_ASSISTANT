import sys
from pathlib import Path
from contextlib import asynccontextmanager

from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession


SERVER_PATH = str(
    Path(__file__).parent / "server.py"
)


@asynccontextmanager
async def get_mcp_client():

    server = StdioServerParameters(
        command=sys.executable,
        args=[SERVER_PATH]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session
