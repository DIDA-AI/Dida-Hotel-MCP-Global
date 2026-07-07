from typing import Annotated, Any, Dict

from fastmcp import FastMCP
from pydantic import Field

from ..auth import extract_api_key
from ..client import request_api
from ..models import DateParam, LocaleParam, OccupancyParam, model_dump


def register_hotel_detail_tool(mcp: FastMCP) -> None:
    @mcp.tool(name="getHotelDetail")
    async def get_hotel_detail(
        hotelId: Annotated[int, Field(description="Hotel unique ID. Use this or `name`; if both are provided, `hotelId` takes priority (obtain it from the searchHotels tool).")] = None,
        name: Annotated[str, Field(description="Hotel name (fuzzy match). Only used when `hotelId` is absent.")] = None,
        dateParam: Annotated[
            DateParam,
            Field(
                description="Check-in / check-out date object. Fields: checkInDate (string, YYYY-MM-DD, pass a valid future date when possible); checkOutDate (string, YYYY-MM-DD, must be later than checkInDate)."
            ),
        ] = None,
        occupancyParam: Annotated[
            OccupancyParam,
            Field(
                description="Guest count and room count object. Fields: adultCount (number, default 2); childCount (number, default 0); childAgeDetails (number[], e.g. [3,5], length should match childCount); roomCount (number, default 1)."
            ),
        ] = None,
        localeParam: Annotated[
            LocaleParam,
            Field(
                description="Country and currency object. Fields: countryCode (string, ISO 3166-1 alpha-2, default CN); currency (string, ISO 4217, default CNY)."
            ),
        ] = None,
    ) -> dict:
        """
        Query real-time room types and pricing for a single hotel (room types, price and tax,
        availability, cancellation policy, etc.). Used for a second price check after the user
        has selected a specific hotel.
        """
        if hotelId is None and not name:
            raise Exception("At least one of `hotelId` or `name` must be provided.")

        api_key = extract_api_key()
        params: Dict[str, Any] = {}

        if hotelId is not None:
            params["hotelId"] = hotelId
        if name:
            params["name"] = name
        if dateParam:
            params["dateParam"] = model_dump(dateParam)
        if occupancyParam:
            params["occupancyParam"] = model_dump(occupancyParam)
        if localeParam:
            params["localeParam"] = model_dump(localeParam)

        return await request_api("POST", "/hoteldetail", api_key, payload=params)
