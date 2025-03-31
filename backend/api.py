from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from agnoagent import movie_agent, MovieResponse, prompt_cache
from utils import normalize_prompt

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/movies/search")
async def search_movies(request: PromptRequest):
    try:
        normalized_prompt = normalize_prompt(request.prompt)

        if normalized_prompt in prompt_cache:
            print("✅ Cache hit")
            return JSONResponse(content=prompt_cache[normalized_prompt])
        
        print("⏳ Fetching fresh response")
        response = movie_agent.run(request.prompt, stream=False)

        # response.content is a MovieResponse object — convert to dict
        if hasattr(response.content, "dict"):  # Pydantic v1
            response_dict = response.content.dict()
        else:
            import json
            response_dict = json.loads(str(response.content))  # Fallback (not ideal)

        # Cache and return
        prompt_cache[normalized_prompt] = response_dict
        return JSONResponse(content=response_dict)

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
