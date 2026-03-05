from fastapi import APIRouter

router = APIRouter()

@router.get('/me')
def me():
    return {"id": 1, "role": "client"}

@router.put('/client/{client_id}')
def update_client(client_id: int, payload: dict):
    return {"client_id": client_id, "updated": payload}

@router.put('/professional/{professional_id}')
def update_professional(professional_id: int, payload: dict):
    return {"professional_id": professional_id, "updated": payload}

@router.put('/advertiser/{advertiser_id}')
def update_advertiser(advertiser_id: int, payload: dict):
    return {"advertiser_id": advertiser_id, "updated": payload}
