import requests

def get_flight_data(search_term, date, end_date, isInternational, nature):
    """
    search_term: e.g. "BERLIN" (will be uppercased)
    date: e.g. "2025-02-15+00%3A54" (or "2025-02-15+00:54" – requests will encode it)
    end_date: e.g. "2025-03-17"
    isInternational: "1" for international, "0" for domestic
    nature: "0" for arrivals, "1" for departures
    """
    url = "https://www.istairport.com/umbraco/api/FlightInfo/GetFlightStatusBoard"

    # Set Referer based on nature:
    # For arrivals (nature="0"), use the arriving-flights page.
    # For departures (nature="1"), use the departure-flights page.
    if nature == "0":
        referer = "https://www.istairport.com/en/flights/flight-info/arriving-flights/?locale=en"
    else:
        referer = "https://www.istairport.com/en/flights/flight-info/departure-flights/?locale=en"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": referer,
        "Cookie": "iga_bid=MDMAAAEANYKlLAAAAACw7TvDp7evZwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJ9F7we45GctjoMKwI5rYgRDoTpA"
    }

    # Ensure the search term is uppercased.
    data = {
        "nature": nature,
        "searchTerm": search_term.upper(),
        "pageSize": "50",
        "isInternational": isInternational,
        "date": date,
        "endDate": end_date,
        "culture": "en",
        "clickedButton": ""
    }

    print("DEBUG - Requesting flight data with parameters:", data)
    print("DEBUG - Requesting flight data with URL:", url)
    print("DEBUG - Requesting flight data with headers:", headers)

    response = requests.post(url, headers=headers, data=data)

    print("\n--- REQUEST INSPECTION ---")
    print("Request URL:", response.request.url)
    print("Request Method:", response.request.method)
    print("Request Headers:", response.request.headers)
    if response.request.body:
        print("Request Body (Raw):", response.request.body)
        # Only decode if the body is bytes:
        try:
            if isinstance(response.request.body, bytes):
                parsed_body = requests.utils.unquote(response.request.body.decode('utf-8'))
            else:
                parsed_body = requests.utils.unquote(response.request.body)
            print("Request Body (Parsed):", parsed_body)
        except Exception as e:
            print("Could not parse request body as URL-encoded:", e)

    return response.json()


# Example usage:
# This call should match your working example for BERLIN arrivals.
result = get_flight_data(
    search_term="BERLIN",
    date="2025-02-15+00%3A54",  # or "2025-02-15+00:54" – requests will encode as needed
    end_date="2025-03-17",
    isInternational="1",
    nature="0"
)
print("DEBUG - FlightData:", result)
