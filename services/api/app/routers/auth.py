from fastapi import APIRouter

router = APIRouter()

@router.post('/register')
def register(payload: dict):
    return {"message": "registered", "user": payload}

@router.post('/login')
def login(payload: dict):
    return {"access_token": "mock-token", "refresh_token": "mock-refresh"}

@router.post('/refresh')
def refresh():
    return {"access_token": "mock-token-2"}

@router.post('/forgot-password')
def forgot_password(payload: dict):
    return {"message": f"recovery sent to {payload.get('email')}"}

@router.post('/reset-password')
def reset_password():
    return {"message": "password updated"}
