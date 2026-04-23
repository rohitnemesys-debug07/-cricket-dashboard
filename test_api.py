import requests

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

headers = {
    "X-RapidAPI-Key": "YOUR_API_KEY",
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

res = requests.get(url, headers=headers)

print("STATUS:", res.status_code)
print("DATA:", res.text)