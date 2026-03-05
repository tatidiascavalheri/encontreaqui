from pydantic import BaseModel, Field

class JobCreate(BaseModel):
    client_id: int
    professional_id: int
    category_id: int
    description: str
    scheduled_at: str

class JobStatusUpdate(BaseModel):
    status: str = Field(pattern="^(requested|accepted|in_progress|completed|canceled_by_client|canceled_by_pro|expired|in_dispute|refunded|paid_out)$")
