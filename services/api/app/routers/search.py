from fastapi import APIRouter, Query
from app.services.proximity import distance_m

router = APIRouter()

SEED_PROS = [
    {"id": 1, "name": "Pro A", "category_id": 1, "lat": -23.5600, "lng": -46.6600, "rating": 4.9, "price": 120},
    {"id": 2, "name": "Pro B", "category_id": 1, "lat": -23.5700, "lng": -46.6500, "rating": 4.6, "price": 100},
    {"id": 3, "name": "Pro C", "category_id": 1, "lat": -23.5800, "lng": -46.6400, "rating": 4.2, "price": 80},
    {"id": 4, "name": "Pro D", "category_id": 1, "lat": -23.5500, "lng": -46.6300, "rating": 4.8, "price": 110},
    {"id": 5, "name": "Pro E", "category_id": 1, "lat": -23.5400, "lng": -46.6200, "rating": 4.4, "price": 90},
]

@router.get('/professionals')
def search_professionals(category_id: int, lat: float = Query(...), lng: float = Query(...), radius_km: float = 20):
    ranked = []
    for pro in SEED_PROS:
        if pro['category_id'] != category_id:
            continue
        dist = distance_m(lat, lng, pro['lat'], pro['lng'])
        if dist <= radius_km * 1000:
            ranked.append({**pro, "distance_m": round(dist, 2)})
    ranked.sort(key=lambda x: x['distance_m'])
    return {"items": ranked}
