from fastmcp import FastMCP

from ..auth import extract_api_key
from ..client import request_api


def register_hotel_search_tags_tool(mcp: FastMCP) -> None:
    @mcp.tool(name="getHotelSearchTags")
    async def get_hotel_search_tags() -> dict:
        """
        Retrieve hotel search tag metadata (AI cache), including the list of available tags.
        Suitable for local caching followed by user-intent parsing, then passing the
        structured tags into `searchHotels.hotelTags`.
        """
        api_key = extract_api_key()
        return await request_api("GET", "/hoteltags", api_key)
