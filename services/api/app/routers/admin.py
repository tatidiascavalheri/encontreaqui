from fastapi import APIRouter

router = APIRouter()

@router.get('/users')
def users():
    return {"items": []}

@router.post('/professionals/{professional_id}/approve')
def approve_professional(professional_id: int):
    return {"professional_id": professional_id, "status": "approved"}

@router.get('/reports/ads')
def ads_report():
    return {"impressions": 0, "clicks": 0, "ctr": 0}
