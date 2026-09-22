from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import sys


class MCPClient:

    def __init__(self):

        self.server_params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "server.main"],
        )

        self.session = None
        self.exit_stack = AsyncExitStack()


    async def connect(self):

        read, write = await self.exit_stack.enter_async_context(
            stdio_client(self.server_params)
        )

        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read, write)
        )

        await self.session.initialize()


    async def list_tools(self):

        response = await self.session.list_tools()

        return response.tools


    async def call_tool(
        self,
        tool_name: str,
        arguments: dict
    ):

        return await self.session.call_tool(
            tool_name,
            arguments
        )


    async def close(self):

        if self.session is not None:
            await self.exit_stack.aclose()
            self.session = None