from typing import Dict, Any
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

class OMDBTools:
    def __init__(self):
        self.api_key = os.getenv("OMDB_API_KEY")
        self.base_url = "http://www.omdbapi.com/"

    async def search_movies(self, query: str) -> Dict[str, Any]:
        """
        Search for movies using the OMDB API
        """
        params = {
            'apikey': self.api_key,
            's': query,
            'type': 'movie'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                return await response.json()

    async def get_movie_details(self, imdb_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific movie
        """
        params = {
            'apikey': self.api_key,
            'i': imdb_id,
            'plot': 'full'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                return await response.json()