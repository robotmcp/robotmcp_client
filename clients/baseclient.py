import asyncio
from dotenv import load_dotenv

from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from llm_store import get_llm
import os

load_dotenv()


MAX_HISTORY = int(os.getenv("MAX_HISTORY", 20))


class MCPClient:
    def __init__(self, llm, command="uv", args=None):
        self.llm = llm
        server_root = os.getenv("ROS_MCP_SERVER_PATH", "")
        if not server_root:
            raise RuntimeError("ROS_MCP_SERVER_PATH not found")

        self.server_params = StdioServerParameters(
            command="uv",
            args=["--directory", f"{server_root}", "run", "server.py"],
            env=os.environ.copy(),
        )
        self.exit_stack = AsyncExitStack()
        self.session = None
        self.agent = None
        self.history = []

    async def setup(self):
        read_write = await self.exit_stack.enter_async_context(
            stdio_client(self.server_params)
        )
        read, write = read_write

        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read, write)
        )
        await self.session.initialize()

        tools = await load_mcp_tools(self.session)

        system_prompt = (
            "You are a ROS 2 robot operator assistant. "
            "You have access to MCP tools that communicate with a live ROS 2 system via rosbridge. "
            "When the user asks you to move the robot or interact with it, act immediately using the available tools — "
            "do not ask for clarification unless a required parameter is genuinely missing. "
            "For movement commands, use /cmd_vel with geometry_msgs/msg/Twist: set linear.x for forward/backward, "
            "angular.z for turning. Reasonable default values: linear.x=0.2 m/s, angular.z=0.5 rad/s. "
            "Always confirm what action you took after calling a tool."
        )

        self.agent = create_agent(self.llm, tools, system_prompt=system_prompt)

        print("MCP Client initialized and connected.")
        return self

    async def serve_query(self, query: str):
        try:
            self.history.append(HumanMessage(content=query))
            response = await self.agent.ainvoke(
                {"messages": self.history},
                config={"recursion_limit": 50},
            )

            all_messages = response.get("messages", [])
            raw = all_messages[-1].content
            if isinstance(raw, list):
                final_answer = " ".join(
                    b["text"]
                    for b in raw
                    if isinstance(b, dict) and b.get("type") == "text"
                )
            else:
                final_answer = raw
            trimmed = list(all_messages)[-MAX_HISTORY:]
            # Always start on a HumanMessage to avoid orphaned tool_call_ids
            for i, msg in enumerate(trimmed):
                if isinstance(msg, HumanMessage):
                    trimmed = trimmed[i:]
                    break
            self.history = trimmed

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
                query = input(">")
                if query.lower() in ("quit", "exit"):
                    break
                await self.serve_query(query)
        finally:
            await self.close()


async def main():
    provider = os.getenv("LLM_PROVIDER")
    llm = get_llm(provider)
    client = MCPClient(llm)
    await client.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
