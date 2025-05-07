# Install dependencies (Run this in your terminal if not installed)
# pip install fastapi uvicorn requests

# from fastapi import FastAPI
# import requests
# import json
# import os

# app = FastAPI()

# API_BASE_URL = "https://youtube-music-api3.p.rapidapi.com"
# HEADERS = {
#     "x-rapidapi-key": "b2fcaf2785msh81507f68e5e85c2p1d97fejsne10a977388bb",
#     "x-rapidapi-host": "youtube-music-api3.p.rapidapi.com"
# }

# @app.get("/music/home")
# def get_music_home():
#     # """Fetches home music data from YouTube Music API."""
#     # try:
#     #     response = requests.get(f"{API_BASE_URL}/v2/home", headers=HEADERS, params={"gl": "ID"})
#     #     response.raise_for_status()  # Raise error if request fails
        
#     #     data = response.json()

#     #     # Save response to a JSON file
#     #     with open("music_home_response.json", "w", encoding="utf-8") as file:
#     #         json.dump(data, file, ensure_ascii=False, indent=4)

#     #     return data

#     # except requests.exceptions.RequestException as e:
#     #     return {"error": str(e)}

#     """Loads saved home data and returns only song items."""
#     try:
#         with open("music_home_response.json", "r", encoding="utf-8") as file:
#             data = json.load(file)
#         return data

#     except Exception as e:
#         return {"error": str(e)}

# @app.get("/music/search")
# def search_music(query: str, search_type: str = "song"):
#     """Searches for music based on a query, uses local cache if available."""
#     cache_file = "music_search_response.json"

#     # ✅ Use cached file if it exists
#     if os.path.exists(cache_file):
#         with open(cache_file, "r", encoding="utf-8") as file:
#             return json.load(file)

#     # 🟡 Otherwise fetch from API
#     try:
#         url = f"{API_BASE_URL}/search"
#         params = {"q": query, "type": search_type}

#         response = requests.get(url, headers=HEADERS, params=params)
#         response.raise_for_status()

#         data = response.json()

#         # Save response to cache
#         with open(cache_file, "w", encoding="utf-8") as file:
#             json.dump(data, file, ensure_ascii=False, indent=4)

#         return data

#     except requests.exceptions.RequestException as e:
#         return {"error": str(e)}

# @app.get("/music/album")
# def get_album_details(browseId: str):
#     try:
#         filename = "album_details_response.json"
#         if os.path.exists(filename):
#             with open(filename, "r", encoding="utf-8") as file:
#                 return json.load(file)

#         url = f"{API_BASE_URL}/getAlbum"
#         params = {"id": browseId}
#         response = requests.get(url, headers=HEADERS, params=params)
#         response.raise_for_status()
#         data = response.json()

#         with open(filename, "w", encoding="utf-8") as file:
#             json.dump(data, file, ensure_ascii=False, indent=4)

#         return data

#     except requests.exceptions.RequestException as e:
#         return {"error": str(e)}

    

# @app.get("/music/playlist")
# def get_playlist_details(browseId: str):
#     try:
#         filename = "playlist_details_response.json"
#         if os.path.exists(filename):
#             with open(filename, "r", encoding="utf-8") as file:
#                 return json.load(file)

#         url = f"{API_BASE_URL}/getPlaylist"
#         params = {"id": browseId}
#         response = requests.get(url, headers=HEADERS, params=params)
#         response.raise_for_status()
#         data = response.json()

#         with open(filename, "w", encoding="utf-8") as file:
#             json.dump(data, file, ensure_ascii=False, indent=4)

#         return data

#     except requests.exceptions.RequestException as e:
#         return {"error": str(e)}



# @app.get("/music/artist")
# def get_artist_details(channelId: str):
#     try:
#         filename = "artist_details_response.json"
#         if os.path.exists(filename):
#             with open(filename, "r", encoding="utf-8") as file:
#                 return json.load(file)

#         url = f"{API_BASE_URL}/getArtists"
#         params = {"id": channelId}
#         response = requests.get(url, headers=HEADERS, params=params)
#         response.raise_for_status()
#         data = response.json()

#         with open(filename, "w", encoding="utf-8") as file:
#             json.dump(data, file, ensure_ascii=False, indent=4)

#         return data

#     except requests.exceptions.RequestException as e:
#         return {"error": str(e)}


# To run the FastAPI server, use the command:
# uvicorn home:app --reload


from fastapi import FastAPI
import requests
import json
import os
import logging
from datetime import datetime
import yt_dlp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama 
from ollama import chat
from ollama import ChatResponse

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

app = FastAPI()

API_BASE_URL = "https://youtube-music-api3.p.rapidapi.com"
HEADERS = {
    "x-rapidapi-key": "b2fcaf2785msh81507f68e5e85c2p1d97fejsne10a977388bb",
    "x-rapidapi-host": "youtube-music-api3.p.rapidapi.com"
}

@app.on_event("startup")
def on_startup():
    """Logs the time when the app starts."""
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"FastAPI app started at {start_time}")

@app.get("/music/home")
def get_music_home():
    """Loads saved home data and returns only song items."""
    try:
        with open("music_home_response.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except Exception as e:
        return {"error": str(e)}

@app.get("/music/search")
def search_music(query: str, search_type: str = "song"):
    """Searches for music based on a query, uses local cache if available."""
    cache_file = "music_search_response.json"

    # # ✅ Use cached file if it exists
    # if os.path.exists(cache_file):
    #     with open(cache_file, "r", encoding="utf-8") as file:
    #         return json.load(file)

    # 🟡 Otherwise fetch from API
    try:
        url = f"{API_BASE_URL}/search"
        params = {"q": query, "type": search_type}

        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()

        data = response.json()

        # Save response to cache
        with open(cache_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.get("/music/album")
def get_album_details(browseId: str):
    try:
        filename = "album_details_response.json"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)

        url = f"{API_BASE_URL}/getAlbum"
        params = {"id": browseId}
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.get("/music/playlist")
def get_playlist_details(browseId: str):
    try:
        filename = "playlist_details_response.json"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)

        url = f"{API_BASE_URL}/getPlaylist"
        params = {"id": browseId}
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.get("/music/artist")
def get_artist_details(channelId: str):
    try:
        filename = "artist_details_response.json"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)

        url = f"{API_BASE_URL}/getArtists"
        params = {"id": channelId}
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    



@app.get("/music/stream_url")
def get_stream_url(videoId: str):
    try:
        ydl_opts = {
            'quiet': True,
            'format': 'bestaudio/best',
            'noplaylist': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={videoId}", download=False)
            audio_url = info.get("url")
        
        return {"audio_url": audio_url}
    
    except Exception as e:
        return {"error": str(e)}




OLLAMA_URL = "http://localhost:11434/api/chat"  # Default Ollama local endpoint
MODEL_NAME = "llama3.1:latest"  # Or any model you have pulled via `ollama pull llama3`

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_with_llm(req: ChatRequest):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": req.message}]
        }, stream=True)

        print(response)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Ollama error")

        full_response = ""
        for line in response.iter_lines():
            if line:
                chunk = line.decode("utf-8")
                try:
                    content = eval(chunk).get("message", {}).get("content")
                    if content:
                        full_response += content
                except:
                    continue

        return {"response": full_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/generate/")
async def generate_text(prompt: str, model: str = MODEL_NAME):
    try:
        response = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}])
        return {"response": response['message']['content']}
    except ollama.ResponseError as e:
            raise HTTPException(status_code=500, detail=f"Ollama API error: {e.error}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Request model
class ChatRequest(BaseModel):
    message: str

# Response model
class ChatReply(BaseModel):
    content: str


import re

@app.post("/chat-ollama", response_model=ChatReply)
def chat_with_llm(req: ChatRequest):
    prompt = (
        "Please try to understand the user's mood based on their message. "
        "Then, recommend a song accordingly, as YouTube might suggest. "
        "Wrap the song in <SongItem> tags. Like <SongItem>Song title</SongItme>"
        "Message: "
    )

    full_message = prompt + req.message
    print(full_message)
    # Step 1: Ask LLM
    response: ChatResponse = chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": full_message}]
    )
    content = response.message["content"]
    print(content)
    # Step 2: Extract song name from <SongItem> tag
    match = re.search(r"<SongItem>(.*?)</SongItem>", content)
    print(f"Match:{match}")
    if not match:
        return ChatReply(content="Muse failed to recommend a song properly.")

    song_name = match.group(1).strip()

    # Step 3: Call /music/search
    try:
        search_response = requests.get(
            "http://localhost:8000/music/search",  # Or your real internal endpoint
            params={"query": song_name, "search_type": "song"}
        )
        search_response.raise_for_status()
        results = search_response.json()  # assumes this is a list of song items

        if not results:
            return ChatReply(content="Couldn't find the song in the music database.")

        # Step 4: Replace <SongItem>...</SongItem> with actual object
        first_song_json = json.dumps(results["result"][0], ensure_ascii=False, indent=2)
        new_content = re.sub(r"<SongItem>.*?</SongItem>", f"<SongItem>{first_song_json}</SongItem>", content)

        print(new_content)

        return ChatReply(content=new_content)

    except Exception as e:
        return ChatReply(content=f"Error fetching song info: {str(e)}")
