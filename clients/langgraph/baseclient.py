# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
import asyncio
from langchain_cerebras import ChatCerebras
import os
from dotenv import load_dotenv
load_dotenv()


async def main():
    server_params = StdioServerParameters(
        command="uv",
        # Make sure to update to the full absolute path to your math_server.py file
        args=["run", "server.py"],
    )
    llm = ChatCerebras(
        model="gpt-oss-120b",
        temperature=0.2,
        max_tokens=10240,
        api_key=os.getenv("CEREBRAS_API_KEY")
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)
            

            # Create and run the agent
            agent = create_agent(llm, tools)
            agent_response = await agent.ainvoke({"messages": "what is the factorial of 3"})
            print(agent_response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())