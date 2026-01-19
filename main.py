from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.utilities.logging import configure_logging


# Create an MCP server
mcp = FastMCP("mcp-server", json_response=True, log_level="ERROR")


# Add an addition tool
@mcp.tool(name="add", title="加法的工具", description="将两个数相加，返回求和结果。")
def add(a: int, b: int) -> int:
    """
    两个数相加。

    args:
        a: int 相加的第一个数字
        b: int 相加的第二个数字
    """
    return f"{a} + {b} = {a + b}"


# 乘法工具
@mcp.tool(name="mul", title="乘法的工具", description="将两个数相乘，返回相乘结果。")
def mul(a: int, b: int) -> int:
    """
    两个数相乘。

    args:
        a: int 相乘的数字
        b: int 相乘的数字
    """
    return f"{a} * {b} = {a * b}"


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def greet(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


# run
def main():
    print("Hello from mcp-server!")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
