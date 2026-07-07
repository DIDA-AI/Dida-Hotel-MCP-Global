from typing import Any, Dict, List

from pydantic import BaseModel, Field


class CheckInParam(BaseModel):
    adultCount: int = Field(default=2, description="Adults per room, integer, >=1. Defaults to 2.")
    checkInDate: str = Field(
        default=None,
        description="Check-in date, format YYYY-MM-DD. Always pass a valid future date when possible.",
    )
    stayNights: int = Field(default=1, description="Number of nights, integer, >=1, max 28. Defaults to 1.")


class FilterOptions(BaseModel):
    distanceInMeter: int = Field(
        default=None,
        description="Distance upper bound in meters, integer, >0. Only meaningful when `place` is a POI-type location. Defaults to 2000 when a POI is used.",
    )
    starRatings: List[float] = Field(
        default=None,
        description="Star rating range array [min, max], 0.0~5.0, step 0.5, with min<=max.",
    )


class HotelTags(BaseModel):
    maxPricePerNight: float = Field(default=None, description="Max price per night (CNY, numeric).")
    preferredBrands: List[str] = Field(
        default=None,
        description="Preferred brands (soft constraint).",
    )
    requiredTags: List[str] = Field(default=None, description="Required tags (hard constraint; non-matching hotels are filtered out).")


class DateParam(BaseModel):
    checkInDate: str = Field(default=None, description="Check-in date, format YYYY-MM-DD. Pass a valid future date when possible.")
    checkOutDate: str = Field(
        default=None,
        description="Check-out date, format YYYY-MM-DD. Must be later than checkInDate.",
    )


class OccupancyParam(BaseModel):
    adultCount: int = Field(default=2, description="Adults per room, integer, >=1. Defaults to 2.")
    childAgeDetails: List[int] = Field(default=None, description="Child ages array, e.g. [3,5]; length should match childCount.")
    childCount: int = Field(default=0, description="Children per room, integer, >=0. Defaults to 0.")
    roomCount: int = Field(default=1, description="Number of rooms, integer, >=1. Defaults to 1.")


class LocaleParam(BaseModel):
    countryCode: str = Field(default="CN", description="ISO 3166-1 alpha-2 country code (uppercase). Defaults to CN.")
    currency: str = Field(default="USD", description="ISO 4217 currency code (uppercase). Defaults to USD.")


def model_dump(data: Any) -> Dict[str, Any]:
    if hasattr(data, "model_dump"):
        return data.model_dump(exclude_none=True)  # pydantic v2
    return data.dict(exclude_none=True)  # pydantic v1
