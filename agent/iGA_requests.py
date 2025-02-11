import requests

def get_flight_data(search_term="null", date="null", end_date="null", isInternational="0", nature = "0"):
    url = "https://www.istairport.com/umbraco/api/FlightInfo/GetFlightStatusBoard"
    
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9,en-GB;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "iga_bid=MDMAAAEAjMEzLAAAAACwIToep5SkZw...",
        "DNT": "1",
        "Origin": "https://www.istairport.com",
        "Pragma": "no-cache",
        "Referer": "https://www.istairport.com/en/flights/flight-info/arriving-flights/?locale=en",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Microsoft Edge\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
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

    response = requests.post(url, headers=headers, data=data)
    # response = requests.post(url, headers=headers, data=data, verify=False) # Bypass SSL verification to avoid SSL errors

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve flight data", "status_code": response.status_code}