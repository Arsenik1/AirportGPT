import requests
import urllib.parse

def get_flight_data(search_term="null", date="null", end_date="null", isInternational="0", nature="0"):

    url = "https://www.istairport.com/umbraco/api/FlightInfo/GetFlightStatusBoard"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "https://www.istairport.com/en/flights/flight-info/arriving-flights/?locale=en",
        "Cookie": "iga_bid=MDMAAAEANYKlLAAAAACw7TvDp7evZwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJ9F7we45GctjoMKwI5rYgRDoTpA"
    }

    data = {
        "nature": nature,
        "searchTerm": search_term,
        "pageSize": "50",
        "isInternational": isInternational,
        "date": date,
        "endDate": end_date,
        "culture": "en",
        "clickedButton": ""
    }

    # print("DEBUG - Requesting flight data with parameters:", data)
    # print("DEBUG - Requesting flight data with URL:", url)
    # print("DEBUG - Requesting flight data with headers:", headers)

    response = requests.request("POST", url, headers=headers, data=data)
    # response = requests.post(url, headers=headers, data=data, verify=False) # Bypass SSL verification to avoid SSL errors

    # print("\n--- REQUEST INSPECTION ---")
    # print("Request URL:", response.request.url)
    # print("Request Method:", response.request.method)
    # print("Request Headers:", response.request.headers)

    # Check the request body (data)
    if response.request.body:
        print("Request Body (Raw):", response.request.body)
        try:
            # Try to parse the body as URL-encoded (common for x-www-form-urlencoded)
            parsed_body = urllib.parse.parse_qs(
                # Decode bytes to string
                response.request.body.decode('utf-8'))
            print("Request Body (Parsed):", parsed_body)
        except Exception as e:
            print("Could not parse request body as URL-encoded:", e)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve flight data", "status_code": response.status_code}
