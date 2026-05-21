from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class HabitBase(BaseModel):
    name: str
    description: Optional[str] = None
    active: Optional[bool] = True

class HabitResponse(HabitBase):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        model_config = {"from_attributes": True}

class HabitLogCreate(BaseModel):
    id_habits: int
    done_date: date

class HabitLogResponse(HabitLogCreate):
    id: int
    id_habits: int
    done_date: date
    created_at: datetime

    class Config:
        model_config = {"from_attributes": True}