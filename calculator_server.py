

from mcp.server.fastmcp import FastMCP

# The server's name is what shows up in the client's tool list / logs.
mcp = FastMCP("Calculator")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers and return the sum.

    Args:
        a: The first number.
        b: The second number.
    """
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a and return the difference.

    Args:
        a: The number to subtract from.
        b: The number to subtract.
    """
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the product.

    Args:
        a: The first number.
        b: The second number.
    """
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b and return the quotient.

    Args:
        a: The numerator.
        b: The denominator. Must not be zero.

    Raises:
        ValueError: If b is zero, since division by zero is undefined.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


if __name__ == "__main__":
    # Default transport is stdio, which is what Claude Desktop and most
    # local MCP clients expect. Change to mcp.run(transport="sse") or
    # "streamable-http" if you need a network-accessible server instead.
    mcp.run()
