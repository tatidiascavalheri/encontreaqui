from fastapi import FastAPI
from app.routers import auth, profiles, search, jobs, chat, ratings, notifications, payments, ads, admin

app = FastAPI(title="EncontreAqui API")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(ratings.router, prefix="/ratings", tags=["ratings"])
app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(ads.router, prefix="/ads", tags=["ads"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
