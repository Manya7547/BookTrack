import asyncio
from fastapi.responses import StreamingResponse
from datetime import datetime

async def event_generator():
    while True:
        yield f"data: Real-time update at {datetime.now()}\n\n"
        await asyncio.sleep(1)

def stream():
    return StreamingResponse(event_generator(), media_type="text/event-stream")
