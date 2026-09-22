from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import StructuredTool
from langchain_core.messages import HumanMessage, ToolMessage
from pydantic import create_model
import asyncio


from client.mcp_client import MCPClient


load_dotenv()


# ============================================================
# Clean MCP result
# ============================================================

def clean_tool_result(result):

    if hasattr(result, "content"):

        text_parts = []

        for item in result.content:

            if hasattr(item, "text"):
                text_parts.append(item.text)

        if text_parts:
            return "\n".join(text_parts)

    return str(result)


# ============================================================
# Convert MCP tool → LangChain tool
# ============================================================

def create_langchain_tool(mcp_client, mcp_tool):

    properties = mcp_tool.inputSchema.get(
        "properties",
        {}
    )

    required_fields = mcp_tool.inputSchema.get(
        "required",
        []
    )

    fields = {}

    for name, schema in properties.items():

        schema_type = schema.get(
            "type",
            "string"
        )

        if schema_type == "integer":
            python_type = int

        elif schema_type == "number":
            python_type = float

        elif schema_type == "boolean":
            python_type = bool

        else:
            python_type = str


        if name in required_fields:
            fields[name] = (
                python_type,
                ...
            )

        else:
            fields[name] = (
                python_type,
                None
            )


    ArgsModel = create_model(
        f"{mcp_tool.name}Args",
        **fields
    )


    async def tool_function(**kwargs):

        result = await mcp_client.call_tool(
            mcp_tool.name,
            kwargs
        )

        return clean_tool_result(result)


    return StructuredTool.from_function(
        coroutine=tool_function,
        name=mcp_tool.name,
        description=mcp_tool.description or "",
        args_schema=ArgsModel
    )


# ============================================================
# Email Agent
# ============================================================

class EmailAgent:

    def __init__(self):

        self.mcp_client = MCPClient()

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            temperature=0
        )

        self.llm_with_tools = None

        self.messages = []


    # --------------------------------------------------------
    # Start agent
    # --------------------------------------------------------

    async def start(self):

        await self.mcp_client.connect()

        print("Connected to MCP server!")


        # Discover MCP tools
        mcp_tools = await self.mcp_client.list_tools()

        print("\nAvailable tools:")

        for tool in mcp_tools:
            print(f"- {tool.name}")


        # Convert MCP tools to LangChain tools
        langchain_tools = []

        for mcp_tool in mcp_tools:

            tool = create_langchain_tool(
                self.mcp_client,
                mcp_tool
            )

            langchain_tools.append(tool)


        # Bind tools to Gemini
        self.llm_with_tools = self.llm.bind_tools(
            langchain_tools
        )


    # --------------------------------------------------------
    # Chat
    # --------------------------------------------------------

    async def chat(self, user_message: str):

        self.messages.append(
            HumanMessage(
                content=user_message
            )
        )


        while True:

            response = await self.llm_with_tools.ainvoke(
                self.messages
            )


            # Add Gemini response
            self.messages.append(response)


            # ------------------------------------------------
            # No tools → final answer
            # ------------------------------------------------

            if not response.tool_calls:

                content = response.content

                if isinstance(content, list):

                    text_parts = []

                    for item in content:

                        if (
                            isinstance(item, dict)
                            and item.get("text")
                        ):
                            text_parts.append(
                                item["text"]
                            )

                    content = "\n".join(text_parts)


                return content


            # ------------------------------------------------
            # Execute tools
            # ------------------------------------------------

            for tool_call in response.tool_calls:

                tool_name = tool_call["name"]
                tool_args = tool_call["args"]


                print(
                    f"Agent is using: {tool_name}"
                )

                print(
                    f"Arguments: {tool_args}"
                )


                result = await self.mcp_client.call_tool(
                    tool_name,
                    tool_args
                )


                clean_result = clean_tool_result(
                    result
                )


                self.messages.append(
                    ToolMessage(
                        content=clean_result,
                        tool_call_id=tool_call["id"]
                    )
                )


    # --------------------------------------------------------
    # Close agent
    # --------------------------------------------------------

    async def close(self):

        await self.mcp_client.close()

import asyncio


async def main():

    agent = EmailAgent()

    await agent.start()

    try:

        while True:

            user_message = input("\nYou: ")

            if user_message.lower() in ["exit", "quit"]:
                break

            response = await agent.chat(
                user_message
            )

            print(f"\nAgent: {response}")

    finally:

        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
