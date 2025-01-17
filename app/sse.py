import asyncio
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

router = APIRouter()

@router.get("/updates/")
async def get_updates():
    async def event_stream():
        while True:
            yield f"data: New book added!\n\n"
            await asyncio.sleep(5)  # Simulates waiting for updates

    return EventSourceResponse(event_stream())