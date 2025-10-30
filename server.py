import asyncio
from mcp.server.fastmcp import FastMCP
import math

# Create the MCP server instance
mcp = FastMCP("factorial-server")

# Define a tool that computes factorial
@mcp.tool()
def factorial(n: int) -> int:
    """
    Compute the factorial of a non-negative integer n.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    return math.factorial(n)

# Start the server
if __name__ == "__main__":
    mcp.run()
