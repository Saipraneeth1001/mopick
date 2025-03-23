from agno.tools import Toolkit
import requests
import os
from typing import Dict, List, Union

class OMDBTools(Toolkit):
    def __init__(self):
        super().__init__(name="omdb_tools")
        self.api_key = os.getenv("OMDB_API_KEY")
        self.base_url = "http://www.omdbapi.com/"
        
        # Debug print to verify API key
        print(f"Initializing OMDBTools with API key: {self.api_key[:5]}...")
        
        # Register the methods as tools
        self.register(self.search_movies)
        self.register(self.get_movie_details)

    def search_movies(self, query: str, page: int = 1) -> str:
        """
        Search for movies by title.
        """
        # We'll fetch 10 movies by making multiple requests if needed
        all_movies = []
        try:
            # First request
            params = {
                'apikey': self.api_key,
                's': query,
                'page': page,
                'type': 'movie'
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('Response') == 'False':
                return f"No movies found for query: {query}. Error: {data.get('Error', 'Unknown error')}"
            
            total_results = int(data.get('totalResults', 0))
            movies = data.get('Search', [])
            all_movies.extend(movies)

            # If we need more movies and there are more pages, fetch them
            while len(all_movies) < 10 and len(all_movies) < total_results and page < 3:
                page += 1
                params['page'] = page
                response = requests.get(self.base_url, params=params)
                data = response.json()
                if data.get('Response') == 'True':
                    all_movies.extend(data.get('Search', []))

            # Take only the first 10 movies
            all_movies = all_movies[:10]
            
            if not all_movies:
                return f"No results found for: {query}"
            
            result = f"Found {len(all_movies)} movies for '{query}':\n\n"
            for idx, movie in enumerate(all_movies, 1):
                # Get detailed information for each movie
                details = self.get_movie_details(movie.get('imdbID'))
                result += f"{idx}. {details}\n"
            
            return result

        except Exception as e:
            return f"Error searching for movies: {str(e)}"

    def get_movie_details(self, movie_id: str) -> str:
        """
        Get detailed information about a specific movie.
        """
        params = {
            'apikey': self.api_key,
            'i': movie_id,
            'plot': 'full'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('Response') == 'False':
                return f"Movie details not found for ID: {movie_id}"
            
            # Create a concise one-line summary
            result = (f"**{data.get('Title')}** ({data.get('Year')}) - "
                     f"Rating: {data.get('imdbRating')}/10, "
                     f"Director: {data.get('Director')}, "
                     f"Genre: {data.get('Genre')}")
            
            return result

        except Exception as e:
            return f"Error fetching movie details: {str(e)}"