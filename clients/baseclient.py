import asyncio
from dotenv import load_dotenv

from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from llm_store import get_llm

load_dotenv()


class MCPClient:
    def __init__(self, llm, command="uv", args=None):
        self.llm = llm
        self.server_params = StdioServerParameters(
            command=command,
            args=args or ["run", "server.py"],
        )
        self.exit_stack = AsyncExitStack()
        self.session = None
        self.agent = None

    async def setup(self):
        # enter the stdio_client context
        read_write = await self.exit_stack.enter_async_context(
            stdio_client(self.server_params)
        )
        read, write = read_write

        # enter the ClientSession context
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read, write)
        )
        await self.session.initialize()

        tools = await load_mcp_tools(self.session)
        self.agent = create_agent(self.llm, tools=tools)

        print("MCP Client initialized and connected.")
        return self

    async def serve_query(self, query: str):
        try:
            response = await self.agent.ainvoke(
                {"messages": [{"role": "user", "content": query}]},
                config={"recursion_limit": 50},
            )
            final_answer = response["messages"][-1].content
            print("Response:", final_answer)
            return final_answer
        except Exception as e:
            print(f"Error in query: {e}")
            return None

    async def close(self):
        await self.exit_stack.aclose()
        print("MCP Client closed.")

    async def run(self):
        await self.setup()
        try:
            while True:
                query = input(">>> ")
                if query.lower() in ("quit", "exit"):
                    break
                await self.serve_query(query)
        finally:
            await self.close()


async def main():
    llm = get_llm("openai")
    client = MCPClient(llm)
    await client.run()


if __name__ == "__main__":
    asyncio.run(main())
