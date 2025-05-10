from typing import Union
import iGA_requests
import datetime
import json
from BooleanAgent import BooleanAgent
from typing import Literal
import re
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class FlightSearchInput(BaseModel):
    search_term: str = Field(
        default="",
        description="Optional: Enter any search term single keyword like city name (e.g., 'London'), flight number (e.g., 'TK1234'), or airport code (e.g., 'IST').")
    isInternational: Literal[True, False, None] = Field(
        default=None,
        description="Optional: Set 'true' for international flights, 'false' for domestic flights.")
    isIstanbulOrigin: Literal[True, False, None] = Field(
        default=None,
        description=(
            "Set to 'true' if the flight originates from Istanbul (i.e., if the query uses 'to [city]'). "
            "Set to 'false' if the flight arrives at Istanbul (i.e., if the query uses 'from [city]')."
        )
    )
    start_date: str = Field(
        default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        description="Optional: Start date and time for the flight search (format: YYYY-MM-DD HH:MM)."
    )
    end_date: str = Field(
        default_factory=lambda: (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
        description="Optional: End date for the flight search (format: YYYY-MM-DD)."
    )
    
def remove_empty_fields(data):
    if isinstance(data, dict):
        # Recursively clean the dictionary and remove empty values
        cleaned_dict = {k: remove_empty_fields(v) for k, v in data.items() if v not in ["", None, [], {}]}
        return cleaned_dict if cleaned_dict else None  # Remove if entire dictionary is empty
    elif isinstance(data, list):
        # Recursively clean the list and remove empty entries
        cleaned_list = [remove_empty_fields(item) for item in data if item not in ["", None, [], {}]]
        return cleaned_list if cleaned_list else None  # Remove list if it ends up empty
    else:
        return data  # Return value as is if not empty

    
def flight_api(search_term: str = "", 
               start_date: Union[datetime.datetime, str] = datetime.datetime.now(), 
               end_date: Union[datetime.datetime, str] = datetime.datetime.now() + datetime.timedelta(days=30),
               isInternational: Literal[True, False, None] = None,
               isIstanbulOrigin: Literal[True, False, None] = None
               ) -> str:
    """Fetches flight data based on the given parameters.

    Args:
        search_term (str, optional): Keyword to search flights (e.g., flight number, airport code).
        start_date (str, optional): Start date and time for the search.
        end_date (str, optional): End date and time for the search.
        isInternational (bool : optional): ''true'' for international flights, 'false' for domestic(Inside Turkey).
        isIstanbulOrigin (bool : optional): 'true' if the flight departs from Istanbul (i.e., 'to [city]'); 
                                 'false' if the flight arrives at Istanbul (i.e., 'from [city]').

    Returns:
        str: Flight information in JSON format.
    """
    # Convert start_date and end_date to formatted strings if they are datetime objects
    if isinstance(start_date, datetime.datetime):
        start_date_str = start_date.strftime("%Y-%m-%d %H:%M")
    else:
        start_date_str = start_date
    if isinstance(end_date, datetime.datetime):
        end_date_str = end_date.strftime("%Y-%m-%d")
    else:
        end_date_str = end_date

    # search_term = re.sub(r'\s+', '+', search_term.upper())
    search_term = search_term.upper()
    
    print("DEBUG - Searching for flights for:", search_term)
    
    # If search_term is a specific flight (e.g., 'TK123'), search all categories.
    if re.match(r"^[A-Z]\d+$", search_term):
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
        all_flights = []
        if isInternational is None and isIstanbulOrigin is None:
            # Both parameters are not provided: try all 4 combinations.
            for intl in [True, False]:
                for dep in [True, False]:
                    flightData = iGA_requests.get_flight_data(
                        search_term,
                        start_date_str,
                        end_date_str,
                        "1" if intl else "0",
                        "1" if dep else "0"
                    )
                    flights = flightData.get("result", {}).get("data", {}).get("flights", [])
                    if flights:
                        all_flights.extend(flights)
        elif isInternational is None:
            # isInternational is not provided: try both True and False with the given isIstanbulOrigin.
            for intl in [True, False]:
                flightData = iGA_requests.get_flight_data(
                    search_term,
                    start_date_str,
                    end_date_str,
                    "1" if intl else "0",
                    "1" if isIstanbulOrigin else "0"
                )
                flights = flightData.get("result", {}).get("data", {}).get("flights", [])
                if flights:
                    all_flights.extend(flights)
        elif isIstanbulOrigin is None:
            # isIstanbulOrigin is not provided: try both True and False with the given isInternational.
            for dep in [True, False]:
                flightData = iGA_requests.get_flight_data(
                    search_term,
                    start_date_str,
                    end_date_str,
                    "1" if isInternational else "0",
                    "1" if dep else "0"
                )
                flights = flightData.get("result", {}).get("data", {}).get("flights", [])
                if flights:
                    all_flights.extend(flights)
        else:
            # Both parameters provided.
            flightData = iGA_requests.get_flight_data(
                search_term,
                start_date_str,
                end_date_str,
                "1" if isInternational else "0",
                "1" if isIstanbulOrigin else "0"
            )
            all_flights = flightData.get("result", {}).get("data", {}).get("flights", [])
            
        print("DEBUG - Combined FlightData:", all_flights)
        response = json.dumps({"flights": all_flights})
    
    # Trim empty attributes from the JSON output
    trimmed_data = remove_empty_fields(json.loads(response))
    cleanedAllFlights = json.dumps(trimmed_data, indent=2)  # Pretty print for debugging
    print("DEBUG - Cleaned Flights:", cleanedAllFlights)

    
    return "FINAL_TOOL_OUTPUT: " + cleanedAllFlights + "\n\n Use this tool output to answer the user query.\n"

FLIGHT_TOOLS = [
    StructuredTool(
        name="Get Flight Information",
        description="""
            Searches for flights at Istanbul Airport based on the given criteria.

            Notes:
            - This system only returns flight data for Istanbul Airport.
            - When the user says 'to [city]', it means the flight departs from Istanbul and goes to that city.
              In that case, set isIstanbulOrigin to 'true'.
            - When the user says 'from [city]', it means the flight originates from that city and arrives at Istanbul.
              In that case, set isIstanbulOrigin to 'false'.
            - International vs. Domestic:
              - International: The flight is going to or coming from a destination outside Turkey.
              - Domestic: The flight is going to or coming from a destination inside Turkey.
            - Boolean values should be used in **lowercase**, e.g., true, false.
            - Use the return value of this tool for the **final answer**.

            Examples:
            1. For international departures from Istanbul to New York:
            {
              "action": "Get Flight Information",
              "action_input": {
                "search_term": "New York",
                "isInternational": true,
                "isIstanbulOrigin": true
              }
            }

            2. For domestic arrivals from Ankara to Istanbul:
            {
              "action": "Get Flight Information",
              "action_input": {
                "search_term": "Ankara",
                "isInternational": false,
                "isIstanbulOrigin": false
              }
            }
        """,
        func= flight_api,
        args_schema=FlightSearchInput
    )
]




# # def listFlights():
#     # TODO: Write this tool to list all flights. When searchTerm is a specific value, the response comes as multiple flights, refer to postman.
#     start_date_str = start_date.strftime("%Y-%m-%d+%H%%3A%M")
#     end_date_str = end_date.strftime("%Y-%m-%d")
#     isInternational = "0"
#     nature = "0"
#     search_term = search_term.upper()
    
    
# TODO: Fetching weather and gate delays can also be an option.