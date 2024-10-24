from pydantic import BaseModel, Field
from typing import List

class PriceModel(BaseModel):
    amount: str
    currency: str

class ItineraryModel(BaseModel):
    id: str
    duration_minutes: int
    price: PriceModel

class SortItinerariesRequest(BaseModel):
    sorting_type: str = Field(..., pattern="^(cheapest|fastest|best)$")
    itineraries: List[ItineraryModel]

class SortItinerariesResponse(BaseModel):
    sorting_type: str
    sorted_itineraries: List[ItineraryModel]