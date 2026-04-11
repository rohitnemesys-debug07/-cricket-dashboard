import requests

def get_matches():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

    headers = {
        "X-RapidAPI-Key": "0ba2479f42msh9d51ba45e7bb989p1fb66ejsn9cbff56b3d07",
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    return response.json()