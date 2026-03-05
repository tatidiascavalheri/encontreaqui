from fastapi import APIRouter, HTTPException
from app.schemas.jobs import JobCreate, JobStatusUpdate

router = APIRouter()
JOBS: dict[int, dict] = {}

@router.post('')
def create_job(payload: JobCreate):
    job_id = len(JOBS) + 1
    JOBS[job_id] = {"id": job_id, **payload.model_dump(), "status": "requested", "history": ["requested"]}
    return JOBS[job_id]

@router.patch('/{job_id}/status')
def update_status(job_id: int, payload: JobStatusUpdate):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail='job not found')
    job['status'] = payload.status
    job['history'].append(payload.status)
    return job

@router.get('/{job_id}')
def get_job(job_id: int):
    return JOBS.get(job_id, {})
