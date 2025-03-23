from agno.agent import Agent, RunResponse
from agno.models.anthropic import Claude
from agno.playground import Playground, serve_playground_app
from agno.storage.agent.sqlite import SqliteAgentStorage
from omdb_tools import OMDBTools
from pydantic import BaseModel
from typing import List, Optional, Iterator

import os
from dotenv import load_dotenv
load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
agent_storage: str = "tmp/agents.db"

class MovieItem(BaseModel):
    title: str
    year: int
    rating: float
    language: str
    genre: str
    director: str
    plot: Optional[str] = None
    awards: Optional[str] = None

class MovieResponse(RunResponse):
    movies: List[MovieItem]
    total_results: int

    def __iter__(self) -> Iterator[str]:
        yield str(self.movies)

movie_agent = Agent(
    name="Movie Agent",
    model=Claude(
        id="claude-3-5-sonnet-20240620",
        api_key=ANTHROPIC_API_KEY
    ),
    tools=[OMDBTools()],
    # response_model=MovieResponse,
    instructions=[
        "You are a movie expert who helps users find and learn about movies.",
        "Include movie ratings, release years",
        "Output should be in a list format, please output around 10 movies",
        "Movie language is not restricted to English, feel free to suggest movies from different languages.",
        "Start with Indian movies but give a response strictly based on rating of the movie.",
        "Format responses in a clear, engaging manner using markdown.",
        "When searching for movies, provide multiple options if available.",
        "Your responses must conform to the MovieResponse model with a list of MovieItem objects.",
        "Each MovieItem must include title, year, rating, language, genre, and director."
    ],
    storage=SqliteAgentStorage(table_name="movie_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

app = Playground(agents=[movie_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("agent:app", reload=True)