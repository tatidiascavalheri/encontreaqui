from fastapi import APIRouter

router = APIRouter()

@router.get('')
def list_notifications(user_id: int):
    return {"user_id": user_id, "items": []}
