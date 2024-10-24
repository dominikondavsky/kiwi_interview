from typing import List, Dict
import logging
import requests

# logger configurations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_exchange_rates(base_currency="EUR"):
    exchange_rates = {}
    try:
        response = requests.get(f"https://v6.exchangerate-api.com/v6/f5a32819a9ecd7b1e4f291fa/latest/{base_currency}")
        if response.status_code == 200:
            data = response.json()
            exchange_rates.update(data['conversion_rates'])
        else:
            logger.error(f"Error in fetching rates: {response.status_code}")
            raise Exception("Unable to fetch exchange rates")
    except Exception as e:
        logger.error(f"Unexpected error fetching rates: {e}")
        raise
    return exchange_rates


def convert_to_eur(itinerary, exchange_rates):
    amount = float(itinerary.price.amount)
    currency = itinerary.price.currency

    # convert to one currency
    if currency != "EUR":
        try:
            if currency in exchange_rates:
                rate = float(exchange_rates[currency])
                amount_in_eur = amount / rate
            else:
                logger.error(f"Rate for currency {currency} not found in exchange rates")
                #iff there is a conversion error, we will use a large value to ensure that this item is not the cheapest
                amount_in_eur = float('inf')
        except Exception as e:
            logger.error(f"Unexpected error converting {currency} to EUR: {e}")
            #iff there is a conversion error, we will use a large value to ensure that this item is not the cheapest
            amount_in_eur = float('inf')
    else:
        amount_in_eur = amount
    logger.info(f"Converted {amount} {currency} to {amount_in_eur} EUR")
    return amount_in_eur


def sort_by_cheapest(itineraries: List[Dict]) -> List[Dict]:
    exchange_rates = get_exchange_rates()
    sorted_itineraries = sorted(itineraries, key=lambda x: convert_to_eur(x, exchange_rates))
    return sorted_itineraries


def sort_by_fastest(itineraries: List[Dict]) -> List[Dict]:
    sorted_itineraries = sorted(itineraries, key=lambda x: x.duration_minutes)
    return sorted_itineraries


"""
My algorithm sorts a list of itineraries by finding an optimal balance between price and duration. 

Steps:
1. first converts all itinerary prices to EUR for easy comparison. Then, it calculates the min and max values for both
2. both price and duration are normalized to a range from 0 to 1, where lower values are better 
3. The final score for each itinerary is the sum of the normalized price and duration scores, which represent a balance between cost and travel time. 
"""
def sort_by_best(itineraries: List[Dict]) -> List[Dict]:
    exchange_rates = get_exchange_rates()
    prices_in_eur = {}

    # convert prices to EUR for all itineraries
    for itinerary in itineraries:
        prices_in_eur[itinerary.id] = convert_to_eur(itinerary,exchange_rates)

    # find the minimum and maximum for price and duration
    min_price = min(prices_in_eur[itinerary.id] for itinerary in itineraries)
    max_price = max(prices_in_eur[itinerary.id] for itinerary in itineraries)
    min_duration = min(itinerary.duration_minutes for itinerary in itineraries)
    max_duration = max(itinerary.duration_minutes for itinerary in itineraries)

    def calculate_score(itinerary):
        price_in_eur = prices_in_eur[itinerary.id]

        # normalize price(range 0-1)
        if max_price == min_price:
            price_score = 0
        else:
            price_score = (price_in_eur - min_price) / (max_price - min_price)

        # normalize duration (range 0-1)
        if max_duration == min_duration:
            duration_score = 0
        else:
            duration_score = (itinerary.duration_minutes - min_duration) / (max_duration - min_duration)

        # sum of price and duration coefficients
        total_score = float(price_score) + float(duration_score)
        return total_score

    sorted_itineraries = sorted(itineraries, key=calculate_score)
    return sorted_itineraries