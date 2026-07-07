from fastmcp import FastMCP

from .hotel_detail import register_hotel_detail_tool
from .hotel_search import register_search_hotels_tool
from .hotel_tags import register_hotel_search_tags_tool


def register_tools(mcp: FastMCP) -> None:
    register_search_hotels_tool(mcp)
    register_hotel_detail_tool(mcp)
    register_hotel_search_tags_tool(mcp)
