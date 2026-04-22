import requests

def get_matches():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

    headers = {
        "X-RapidAPI-Key": "YOUR_API_KEY",
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {}
