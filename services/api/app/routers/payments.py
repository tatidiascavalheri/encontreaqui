from fastapi import APIRouter
from app.services.payments import PaymentProvider

router = APIRouter()
provider = PaymentProvider()

@router.post('/intent')
def create_intent(payload: dict):
    return provider.create_intent(payload['amount_cents'])

@router.post('/webhook')
def webhook(payload: dict):
    return {"received": True, "event": payload.get('type')}

@router.post('/payout/{job_id}')
def payout(job_id: int):
    return {"job_id": job_id, "status": "scheduled"}
