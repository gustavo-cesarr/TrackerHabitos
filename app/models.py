from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Date, Datetime, Time
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql import func


class Habit(Base):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    active = Column(Boolean, default=True, nullable=False)
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")

class HabitLog(Base):
    __tablename__ = 'habits_logs'
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey('habits.id'), nullable=False)
    done_date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    habit = relationship("Habit", back_populates="logs")
