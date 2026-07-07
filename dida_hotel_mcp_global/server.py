import os

from dotenv import load_dotenv
from fastmcp import FastMCP

from .tools import register_tools

load_dotenv()

mcp = FastMCP("Dida Hotel MCP", version="1.0.0")
register_tools(mcp)


def main() -> None:
    print("Dida Hotel MCP Server starting...")
    print("Auth: reads Authorization / X-Secret-Key from the request header")
    mcp.run(
        transport="http",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
    )


if __name__ == "__main__":
    main()
