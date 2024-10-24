from fastapi import FastAPI, HTTPException
from typing import List
from models import SortItinerariesRequest, SortItinerariesResponse
from services import sort_by_cheapest, sort_by_fastest, sort_by_best

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/sort_itineraries", response_model=SortItinerariesResponse)
async def sort_itineraries(request: SortItinerariesRequest):
    sorting_type = request.sorting_type
    itineraries = request.itineraries

    # Sorting logic
    if sorting_type == "cheapest":
        sorted_itineraries = sort_by_cheapest(itineraries)
    elif sorting_type == "fastest":
        sorted_itineraries = sort_by_fastest(itineraries)
    elif sorting_type == "best":
        sorted_itineraries = sort_by_best(itineraries)
    else:
        raise HTTPException(status_code=400, detail="Invalid sorting type")

    return SortItinerariesResponse(sorting_type=sorting_type, sorted_itineraries=sorted_itineraries)