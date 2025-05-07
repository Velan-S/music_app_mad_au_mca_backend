import http.client
import json

# API connection setup
conn = http.client.HTTPSConnection("youtube-music-api3.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "b2fcaf2785msh81507f68e5e85c2p1d97fejsne10a977388bb",
    'x-rapidapi-host': "youtube-music-api3.p.rapidapi.com"
}

# Make the API request
conn.request("GET", "/search_suggestions?q=7%20years", headers=headers)

# Get the response
res = conn.getresponse()
data = res.read()

# Decode and parse JSON
parsed_data = json.loads(data.decode("utf-8"))

# Save to a JSON file
with open("search_results.json", "w", encoding="utf-8") as json_file:
    json.dump(parsed_data, json_file, indent=4, ensure_ascii=False)

print("✅ Data saved to 'search_results.json'")
