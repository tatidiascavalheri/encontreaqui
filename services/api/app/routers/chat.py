from fastapi import APIRouter, WebSocket

router = APIRouter()

@router.get('/threads/{job_id}')
def get_thread(job_id: int):
    return {"job_id": job_id, "messages": []}

@router.post('/threads/{job_id}/messages')
def send_message(job_id: int, payload: dict):
    return {"job_id": job_id, "message": payload, "delivered": True}

@router.websocket('/ws/{job_id}')
async def job_ws(websocket: WebSocket, job_id: int):
    await websocket.accept()
    while True:
        msg = await websocket.receive_text()
        await websocket.send_text(f"job:{job_id}:{msg}")
