from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.playground import Playground, serve_playground_app
from agno.storage.agent.sqlite import SqliteAgentStorage
from omdb_tools import OMDBTools
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv
import json

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
agent_storage = "agent_storage.db"

class MovieItem(BaseModel):
    title: str
    year: int
    rating: float
    language: str
    genre: str
    # director: str
    # plot: Optional[str] = None
    # awards: Optional[str] = None

class MovieResponse(BaseModel):
    movies: List[MovieItem] = Field(default_factory=list)
    total_results: int = 0

movie_agent = Agent(
    name="Movie Agent",
    model=Claude(
        id="claude-3-5-sonnet-20240620",
        api_key=ANTHROPIC_API_KEY
    ),
    tools=[OMDBTools()],
    response_model=MovieResponse,
    instructions=[
        "You are a movie expert who helps users find and learn about movies.",
        "Always structure your response as a valid MovieResponse object with movies list and total_results.",
        "Each movie must include:",
        "- title (string)",
        "- year (integer)",
        "- rating (float)",
        "- language (string)",
        "- genre (string)",
        "- director (string)",
        "Optional fields are plot and awards.",
        "Include movie ratings and release years",
        "Provide around 10 movies in each response",
        "Movie language is not restricted to English",
        "Start with Indian movies but give a response strictly based on rating of the movie."
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