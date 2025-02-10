from typing import Optional
import iGA_requests
from langchain_ollama import ChatOllama
import iGA_globals
import datetime
import json
from BooleanAgent import BooleanAgent
from typing import Literal
import re

def flight_api(search_term: str = "changeFlight", 
               start_date: datetime.datetime = datetime.datetime.now(), 
               end_date: datetime.datetime = datetime.datetime.now() + datetime.timedelta(days=30),
               isInternational: Literal[True, False] = False,
               isDeparture: Literal[True, False] = False
               ) -> str:
    """Fetches flight data based on the given parameters.

    Args:
        search_term (str : optional): Keyword to search flights (e.g., flight number, airport code).
        start_date (datetime : optional): Start date and time for the search.
        end_date (datetime : optional): End date and time for the search.
        isInternational (bool : optional): true for international flights, false for domestic.
        isDeparture (bool : optional): true for departure flights, false for arrival.

    Returns:
        str: Flight information in English.
    """
    start_date_str = start_date.strftime("%Y-%m-%d+%H%%3A%M")
    end_date_str = end_date.strftime("%Y-%m-%d")
    isInternationalStr = "1" if isInternational else "0"
    nature = "1" if isDeparture else "0"
    search_term = search_term.upper()
    
    print("DEBUG - Searching for flights with search term: " + search_term + " between " + start_date_str + " and " + end_date_str)
    
    booleanAgent = BooleanAgent()

    print("DEBUG - Trying domestic arrival flights")
    flightData = iGA_requests.get_flight_data(search_term, start_date_str, end_date_str)
    verification_prompt = "Return true if there are any flights listed in here: " + str(flightData) + "\". Otherwise, return false."
    
    if booleanAgent.run(verification_prompt) == "False":
        print("DEBUG - No flights found, trying international arrival flights")
        isInternationalStr = "1"
        flightData = iGA_requests.get_flight_data(search_term, start_date_str, end_date_str, isInternationalStr)
        
        verification_prompt_international = "Return true if there are any flights listed in here: " + str(flightData) + "\". Otherwise, return false."
        if booleanAgent.run(verification_prompt_international) == "False":
            print("DEBUG - No international flights found, trying domestic departure flights")
            isInternationalStr = "0"
            nature = "1"
            flightData = iGA_requests.get_flight_data(search_term, start_date_str, end_date_str, isInternationalStr, nature)

            verification_prompt_nature = "Return true if there are any flights listed in here: " + str(flightData) + "\". Otherwise, return false."
            if booleanAgent.run(verification_prompt_nature) == "False":
                print("DEBUG - No nature flights found, trying international departure flights")
                isInternationalStr = "1"
                nature = "1"
                flightData = iGA_requests.get_flight_data(search_term, start_date_str, end_date_str, isInternationalStr, nature)

    # announce_message = "Translate the following JSON flight data into a clear, plain-text description. Include all flight information accurately without any JSON formatting, so that it is easily understandable by another LLM:"
    # flight_data_json = [announce_message + json.dumps(flightData)]
    # response = "Get Flight Information Tool's Return string: \"" + iGA_globals.chatState.model.invoke(flight_data_json).content + "\""
    
    # if iGA_globals.chatState.modelName.lower().startswith("deepseek"):
    #     response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)
    
    response = json.dumps(flightData)

    print("DEBUG" + response)
    return response

# # def listFlights():
#     # TODO: Write this tool to list all flights. When searchTerm is a specific value, the response comes as multiple flights, refer to postman.
#     start_date_str = start_date.strftime("%Y-%m-%d+%H%%3A%M")
#     end_date_str = end_date.strftime("%Y-%m-%d")
#     isInternational = "0"
#     nature = "0"
#     search_term = search_term.upper()
    
    
# TODO: Fetching weather and gate delays can also be an option.