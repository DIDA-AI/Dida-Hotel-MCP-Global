from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from ..auth import extract_api_key
from ..client import request_api
from ..models import CheckInParam, FilterOptions, HotelTags, model_dump


def register_search_hotels_tool(mcp: FastMCP) -> None:
    @mcp.tool(name="searchHotels")
    async def search_hotels(
        originQuery: Annotated[str, Field(description="The user's original natural-language query (verbatim), used for semantic understanding and ranking.")],
        place: Annotated[
            str,
            Field(
                description="A single geocodeable location text defining the search scope, e.g. \"Beijing\", \"Shanghai Pudong International Airport\", \"Tokyo Disneyland\", \"No. 19 Sanlitun Road, Chaoyang District, Beijing\"."
            ),
        ],
        placeType: Annotated[
            str,
            Field(description="Location type. Allowed values: `city`, `airport`, `point_of_interest`, `train_station`, `subway_station`, `hotel`, `district/county`, `detailed address`. Must be semantically consistent with `place`."),
        ],
        checkInParam: Annotated[
            CheckInParam,
            Field(
                description="Check-in parameter object. Fields: adultCount (number, default 2); checkInDate (string, YYYY-MM-DD); stayNights (number, default 1)."
            ),
        ] = None,
        countryCode: Annotated[str, Field(description="ISO 3166-1 alpha-2 country code (uppercase), e.g. CN, US, JP. Pass when a country name is ambiguous or to explicitly scope to a country.")] = None,
        filterOptions: Annotated[
            FilterOptions,
            Field(
                description="Basic filter object. Fields: distanceInMeter (number, distance upper bound in meters); starRatings (number[], star range [min,max], 0.0~5.0, step 0.5)."
            ),
        ] = None,
        hotelTags: Annotated[
            HotelTags,
            Field(
                description="Tag filter object (advanced filters). Fields: requiredTags (string[], required tags, hard constraint); preferredBrands (string[], preferred brands); maxPricePerNight (number, nightly budget cap in CNY)."
            ),
        ] = None,
        size: Annotated[int, Field(description="Upper bound on the number of hotels returned. Pass an integer in 5-20; defaults to 5.")] = 5,
    ) -> dict:
        """
        Search hotels worldwide. Returns a candidate hotel list with the lowest price for each,
        based on the location and structured filters (dates, nights, guests, star rating,
        distance, tags, brands, budget). Used for initial hotel screening and comparison.
        """
        api_key = extract_api_key()

        params = {
            "originQuery": originQuery,
            "place": place,
            "placeType": placeType,
            "size": size,
        }

        if checkInParam:
            params["checkInParam"] = model_dump(checkInParam)

        if countryCode:
            params["countryCode"] = countryCode

        if filterOptions:
            params["filterOptions"] = model_dump(filterOptions)

        if hotelTags:
            params["hotelTags"] = model_dump(hotelTags)

        return await request_api("POST", "/hotelsearch", api_key, payload=params)
