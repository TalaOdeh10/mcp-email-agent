from mcp.server.fastmcp import FastMCP

from server.tools.email_tools import (
    list_emails,
    search_emails,
    get_email,
)


mcp = FastMCP("Email Server")


@mcp.tool()
def hello(name: str) -> str:
    """Say hello to a user."""

    return f"Hello, {name}!"


mcp.tool()(list_emails)
mcp.tool()(search_emails)
mcp.tool()(get_email)


if __name__ == "__main__":
    mcp.run(transport="stdio")