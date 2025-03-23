from typing import Dict, List, Optional
from agno.tools import Toolkit
import requests
import os

class IMDBTools(Toolkit):
    def __init__(self):
        super().__init__(name="imdb_tools")
        self.api_endpoint = "https://api.imdb.com/graphql"  # Replace with actual IMDb GraphQL endpoint
        self.api_key = os.getenv("IMDB_API_KEY")
        
        # Register the methods as tools
        self.register(self.search_titles)
        self.register(self.get_title_details)
        self.register(self.search_names)

    def search_titles(self, query: str, limit: int = 10) -> Dict:
        """
        Search for movies, TV shows, and other titles on IMDb.

        Args:
            query (str): Search term for titles
            limit (int): Maximum number of results to return (default: 10)
        Returns:
            dict: Search results containing title information
        """
        query = """
        query SearchTitles($searchTerm: String!, $limit: Int!) {
            titleSearch(term: $searchTerm, limit: $limit) {
                results {
                    id
                    titleText {
                        text
                    }
                    releaseYear {
                        year
                    }
                    titleType {
                        text
                    }
                }
            }
        }
        """
        variables = {
            "searchTerm": query,
            "limit": limit
        }
        return self._execute_query(query, variables)

    def get_title_details(self, title_id: str) -> Dict:
        """
        Get detailed information about a specific title.

        Args:
            title_id (str): The IMDb ID of the title (e.g., 'tt0111161')
        Returns:
            dict: Detailed title information including plot, ratings, cast, etc.
        """
        query = """
        query GetTitleDetails($id: ID!) {
            title(id: $id) {
                id
                titleText {
                    text
                }
                plot {
                    plotText {
                        plainText
                    }
                }
                ratingsSummary {
                    aggregateRating
                    voteCount
                }
                releaseYear {
                    year
                }
                runtime {
                    seconds
                }
                genres {
                    genres {
                        text
                    }
                }
            }
        }
        """
        variables = {"id": title_id}
        return self._execute_query(query, variables)

    def search_names(self, query: str, limit: int = 10) -> Dict:
        """
        Search for people (actors, directors, etc.) on IMDb.

        Args:
            query (str): Search term for names
            limit (int): Maximum number of results to return (default: 10)
        Returns:
            dict: Search results containing person information
        """
        query = """
        query SearchNames($searchTerm: String!, $limit: Int!) {
            nameSearch(term: $searchTerm, limit: $limit) {
                results {
                    id
                    nameText {
                        text
                    }
                    primaryProfession {
                        text
                    }
                }
            }
        }
        """
        variables = {
            "searchTerm": query,
            "limit": limit
        }
        return self._execute_query(query, variables)

    def _execute_query(self, query: str, variables: Dict) -> Dict:
        """
        Execute a GraphQL query against the IMDb API.
        """
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }
        
        try:
            response = requests.post(
                self.api_endpoint,
                json={
                    "query": query,
                    "variables": variables
                },
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"API request failed: {str(e)}"}

    def get_tools(self):
        """Return list of available tools"""
        return [
            {
                "name": "search_titles",
                "description": "Search for movies, TV shows, and other titles on IMDb",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The search term"},
                        "limit": {"type": "integer", "description": "Maximum number of results to return (default: 10)"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_title_details",
                "description": "Get detailed information about a specific title",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title_id": {"type": "string", "description": "The IMDb ID of the title"}
                    },
                    "required": ["title_id"]
                }
            },
            {
                "name": "search_names",
                "description": "Search for people (actors, directors, etc.) on IMDb",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The search term"},
                        "limit": {"type": "integer", "description": "Maximum number of results to return (default: 10)"}
                    },
                    "required": ["query"]
                }
            }
        ]