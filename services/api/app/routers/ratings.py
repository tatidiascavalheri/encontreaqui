from fastapi import APIRouter, HTTPException

router = APIRouter()
RATINGS = []

@router.post('')
def create_rating(payload: dict):
    if payload.get('job_status') != 'completed':
        raise HTTPException(status_code=400, detail='rating only after completed job')
    key = (payload.get('job_id'), payload.get('rater_id'), payload.get('target_id'))
    if any((r['job_id'], r['rater_id'], r['target_id']) == key for r in RATINGS):
        raise HTTPException(status_code=400, detail='duplicate rating')
    RATINGS.append(payload)
    return payload

@router.get('/summary/{user_id}')
def summary(user_id: int):
    user_ratings = [r for r in RATINGS if r.get('target_id') == user_id]
    count = len(user_ratings)
    avg = sum(r.get('score', 0) for r in user_ratings) / count if count else 0
    return {"user_id": user_id, "count": count, "average": round(avg, 2)}
