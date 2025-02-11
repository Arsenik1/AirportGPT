from typing import Optional, Union
import iGA_requests
from langchain_ollama import ChatOllama
import iGA_globals
import datetime
import json
from BooleanAgent import BooleanAgent
from typing import Literal
import re

def flight_api(search_term: str = "changeFlight", 
               start_date: Union[datetime.datetime, str] = datetime.datetime.now(), 
               end_date: Union[datetime.datetime, str] = datetime.datetime.now() + datetime.timedelta(days=30),
               isInternational: Literal[True, False] = False,
               isDeparture: Literal[True, False] = False
               ) -> str:
    """Fetches flight data based on the given parameters.

    Args:
        search_term (str : optional): Keyword to search flights (e.g., flight number, airport code).
        start_date (datetime : optional): Start date and time for the search.
        end_date (datetime : optional): End date and time for the search.
        isInternational (bool : optional): 'true' for international flights, 'false' for domestic(Inside Turkey).
        isDeparture (bool : optional): 'true' for Istanbul departure flights, 'false' for arrival.

    Returns:
        str: Flight information in English.
    """
    # Convert start_date and end_date to formatted strings if they are datetime objects
    if isinstance(start_date, datetime.datetime):
        start_date_str = start_date.strftime("%Y-%m-%d+%H%%3A%M")
    else:
        start_date_str = start_date
    if isinstance(end_date, datetime.datetime):
        end_date_str = end_date.strftime("%Y-%m-%d")
    else:
        end_date_str = end_date

    search_term = search_term.upper()
    
    print("DEBUG - Searching for flights for:", search_term)
    
    # If search_term is a specific flight (e.g., 'TK123'), search all categories.
    if re.match(r"^[A-Z]{2}\d+$", search_term):
        categories = [
            {"isInternational": "0", "nature": "0"},  # domestic arrival
            {"isInternational": "1", "nature": "0"},  # international arrival
            {"isInternational": "0", "nature": "1"},  # domestic departure
            {"isInternational": "1", "nature": "1"}   # international departure
        ]
        all_flights = []
        for cat in categories:
            print("DEBUG - Checking category: isInternational:", cat["isInternational"], "nature:", cat["nature"])
            flightData = iGA_requests.get_flight_data(search_term, start_date_str, end_date_str, cat["isInternational"], cat["nature"])
            print("DEBUG - FlightData for this category:", flightData)
            flights = flightData.get("result", {}).get("data", {}).get("flights", [])
            if flights:
                all_flights.extend(flights)
        response = json.dumps({"flights": all_flights})
    else:
        # Otherwise, list flights matching the search term using provided parameters.
        flightData = iGA_requests.get_flight_data(
            search_term,
            start_date_str,
            end_date_str,
            "1" if isInternational else "0",
            "1" if isDeparture else "0"
        )
        response = json.dumps(flightData.get("result", {}).get("data", {}).get("flights", []))
    
    print("DEBUG - Result:", response)
    return response

# # def listFlights():
#     # TODO: Write this tool to list all flights. When searchTerm is a specific value, the response comes as multiple flights, refer to postman.
#     start_date_str = start_date.strftime("%Y-%m-%d+%H%%3A%M")
#     end_date_str = end_date.strftime("%Y-%m-%d")
#     isInternational = "0"
#     nature = "0"
#     search_term = search_term.upper()
    
    
# TODO: Fetching weather and gate delays can also be an option.