import os
import asyncio
from dotenv import load_dotenv
from agno.agent import RunResponse
from agno.models.anthropic import Claude
from typing import AsyncIterator

load_dotenv()  # If you have a .env with ANTHROPIC_API_KEY

class FixedAgent:
    """
    A minimal Agent-like class demonstrating the needed run/arun logic.
    Uses a simple Claude model example.
    """

    def __init__(self, anthropic_api_key: str):
        self.model = Claude(id="claude-2", api_key=anthropic_api_key)

    async def _stream_response_iter(self, prompt: str, **kwargs) -> AsyncIterator[RunResponse]:
        """Internal async generator that yields partial chunks from the model."""
        async for model_chunk in self.model.ainvoke_stream(prompt, **kwargs):
            # If the chunk is a string, wrap in RunResponse
            if isinstance(model_chunk, RunResponse):
                yield model_chunk
            else:
                yield RunResponse(content=model_chunk)

    async def arun(self, prompt: str, stream: bool = False, **kwargs):
        """Asynchronous run: streaming or non-streaming."""
        if stream:
            return self._stream_response_iter(prompt, **kwargs)
        else:
            result = await self.model.ainvoke(prompt, **kwargs)
            return result if isinstance(result, RunResponse) else RunResponse(content=result)

    def run(self, prompt: str, stream: bool = False, **kwargs):
        """Synchronous run: streaming or non-streaming."""
        if stream:
            # Return an async generator for streaming
            return self._stream_response_iter(prompt, **kwargs)
        else:
            result = self.model.invoke(prompt, **kwargs)
            return result if isinstance(result, RunResponse) else RunResponse(content=result)

# --------------------------------------------------------
# EXAMPLE USAGE
# --------------------------------------------------------
if __name__ == "__main__":
    # Make sure you have your Anthropic API key exported or in .env
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "YOUR_KEY_HERE")
    agent = FixedAgent(anthropic_api_key=ANTHROPIC_API_KEY)

    prompt = "Tell me about the best Indian thriller movies from the past decade."

    # 1) Non-streaming usage
    response = agent.run(prompt)
    print("Non-streaming (synchronous) response:\n", response.content)

    # 2) Streaming usage in an async context
    async def test_stream():
        # We'll demonstrate an asynchronous for loop
        chunk_iter = agent.run(prompt, stream=True)
        async for chunk in chunk_iter:
            print("STREAMING CHUNK:", chunk.content)

    asyncio.run(test_stream())
