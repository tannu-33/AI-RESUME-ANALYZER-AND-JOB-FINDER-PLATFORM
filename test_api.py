import requests

API_KEY = "YOUR_REAL_RAPIDAPI_KEY"

url = "https://jsearch.p.rapidapi.com/search"

querystring = {
    "query": "Software Engineer in India",
    "page": "1",
    "num_pages": "1"
}

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print("Status Code:", response.status_code)
print("Response:", response.text[:1000])