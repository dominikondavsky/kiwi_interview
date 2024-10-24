import pytest
from fastapi.testclient import TestClient
from main import app

from services import convert_to_eur, sort_by_cheapest, sort_by_fastest, sort_by_best
from models import PriceModel, ItineraryModel

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}


# Unit tests for individual functions
def test_convert_to_eur():
    exchange_rates = {"USD": "1.2"}
    itinerary = ItineraryModel(id="1", duration_minutes=60, price=PriceModel(amount="100", currency="USD"))
    amount_in_eur = convert_to_eur(itinerary, exchange_rates)
    assert amount_in_eur == float(100/1.2)


def test_sort_by_cheapest():
    itineraries = [
        ItineraryModel(id="1", duration_minutes=120, price=PriceModel(amount="100", currency="USD")),
        ItineraryModel(id="2", duration_minutes=150, price=PriceModel(amount="80", currency="EUR")),
    ]
    sorted_itineraries = sort_by_cheapest(itineraries)
    assert sorted_itineraries[0].id == "2"


def test_sort_by_fastest():
    itineraries = [
        ItineraryModel(id="1", duration_minutes=120, price=PriceModel(amount="100", currency="EUR")),
        ItineraryModel(id="2", duration_minutes=100, price=PriceModel(amount="150", currency="EUR")),
    ]
    sorted_itineraries = sort_by_fastest(itineraries)
    assert sorted_itineraries[0].id == "2"


def test_sort_by_best():
    itineraries = [
        ItineraryModel(id="1", duration_minutes=120, price=PriceModel(amount="100", currency="EUR")),
        ItineraryModel(id="2", duration_minutes=150, price=PriceModel(amount="80", currency="EUR")),
        ItineraryModel(id="3", duration_minutes=121, price=PriceModel(amount="85", currency="EUR")),
    ]
    sorted_itineraries = sort_by_best(itineraries)
    assert sorted_itineraries[0].id == "3"


# Test sorting endpoint
@pytest.mark.parametrize("sorting_type", ["cheapest", "fastest", "best"])
def test_sort_itineraries_endpoint(sorting_type):
    response = client.post(
        "/sort_itineraries",
        json={
            "sorting_type": sorting_type,
            "itineraries": [
                {
                "id": "moja_1",
                "duration_minutes": 1,
                "price": {
                    "amount": "1",
                    "currency": "EUR"
                }
                },
                {
                "id": "moja_2",
                "duration_minutes": 25,
                "price": {
                    "amount": "25",
                    "currency": "EUR"
                }
                },
                {
                "id": "moja_3",
                "duration_minutes": 10,
                "price": {
                    "amount": "10.0",
                    "currency": "CZK"
                }
                },
                {
                "id": "moja_4",
                "duration_minutes": 3,
                "price": {
                    "amount": "40.0",
                    "currency": "PLN"
                }
                }
            ]
        },
    )
    assert response.status_code == 200
    if sorting_type == "cheapest":
        assert response.json() == {
            "sorting_type": "cheapest",
            "sorted_itineraries": [
                {
                    "id": "moja_3",
                    "duration_minutes": 10,
                    "price": {
                        "amount": "10.0",
                        "currency": "CZK"
                    }
                },
                {
                    "id": "moja_1",
                    "duration_minutes": 1,
                    "price": {
                        "amount": "1",
                        "currency": "EUR"
                    }
                },
                {
                    "id": "moja_4",
                    "duration_minutes": 3,
                    "price": {
                        "amount": "40.0",
                        "currency": "PLN"
                    }
                },
                {
                    "id": "moja_2",
                    "duration_minutes": 25,
                    "price": {
                        "amount": "25",
                        "currency": "EUR"
                    }
                }
            ]
        }
    elif sorting_type == "fastest":
        assert response.json() == {
            "sorting_type": "fastest",
            "sorted_itineraries": [
                {
                    "id": "moja_1",
                    "duration_minutes": 1,
                    "price": {
                        "amount": "1",
                        "currency": "EUR"
                    }
                },
                {
                    "id": "moja_4",
                    "duration_minutes": 3,
                    "price": {
                        "amount": "40.0",
                        "currency": "PLN"
                    }
                },
                {
                    "id": "moja_3",
                    "duration_minutes": 10,
                    "price": {
                        "amount": "10.0",
                        "currency": "CZK"
                    }
                },
                {
                    "id": "moja_2",
                    "duration_minutes": 25,
                    "price": {
                        "amount": "25",
                        "currency": "EUR"
                    }
                }
            ]
        }
    elif sorting_type == "best":
        assert response.json() == {
            "sorting_type": "best",
            "sorted_itineraries": [
                {
                    "id": "moja_1",
                    "duration_minutes": 1,
                    "price": {
                        "amount": "1",
                        "currency": "EUR"
                    }
                },
                {
                    "id": "moja_3",
                    "duration_minutes": 10,
                    "price": {
                        "amount": "10.0",
                        "currency": "CZK"
                    }
                },
                {
                    "id": "moja_4",
                    "duration_minutes": 3,
                    "price": {
                        "amount": "40.0",
                        "currency": "PLN"
                    }
                },
                {
                    "id": "moja_2",
                    "duration_minutes": 25,
                    "price": {
                        "amount": "25",
                        "currency": "EUR"
                    }
                }
            ]
        }


def test_sort_itineraries_invalid_sorting_type():
    response = client.post(
        "/sort_itineraries",
        json={
            "sorting_type": "invalid_type",
            "itineraries": []
        },
    )
    assert response.status_code == 422