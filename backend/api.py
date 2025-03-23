from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from agent import movie_agent, MovieResponse, MovieItem
import json

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/movies/search")
async def search_movies(request: PromptRequest):
    try:
        # Get the response from the agent
        run_response = await movie_agent.arun(request.prompt)
        
        # Extract the content from RunResponse
        content = run_response.content
        
        try:
            # Parse the content as JSON
            if isinstance(content, str):
                response_data = json.loads(content)
            else:
                response_data = content.dict()
                
            # Create MovieResponse object
            movie_response = MovieResponse(**response_data)
            return movie_response.dict()
            
        except Exception as e:
            print(f"Raw content: {content}")
            print(f"Error during parsing: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse response content: {str(e)}"
            )
            
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
