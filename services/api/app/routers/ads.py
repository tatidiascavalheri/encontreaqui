from fastapi import APIRouter
import random

router = APIRouter()

ADS = [
    {"id": 1, "placement": "HOME", "status": "active", "role": "client", "city": "SP", "weight": 2},
    {"id": 2, "placement": "HOME", "status": "active", "role": "client", "city": "SP", "weight": 1},
]

@router.get('/serve')
def serve(placement: str, lat: float, lng: float, role: str):
    pool = [a for a in ADS if a['placement'] == placement and a['status'] == 'active' and a['role'] == role]
    weights = [a['weight'] for a in pool]
    selected = random.choices(pool, weights=weights, k=1)[0] if pool else None
    return {"ad": selected}

@router.post('/track/impression')
def impression(payload: dict):
    return {"tracked": "impression", **payload}

@router.post('/track/click')
def click(payload: dict):
    return {"tracked": "click", **payload}

@router.get('/advertiser/campaigns')
def campaigns():
    return {"items": ADS}
