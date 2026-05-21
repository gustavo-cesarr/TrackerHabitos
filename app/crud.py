from sqlalchemy.orm import Session
from app import models, schemas
from datetime import date
from app.models import Habit

def get_habit(db: Session, habit_id: int):
    return db.query(models.Habit).filter(models.Habit.id == habit_id).first()

def get_habits(db: Session):
    return db.query(models.Habit).all()    

def get_habit_by_id(db: Session, habit_id: int):
    return db.query(models.Habit).filter(models.Habit.id == habit_id).first()

def create_habit(db: Session, habit: schemas.HabitBase):
    db_habit = models.Habit(name=habit.name, description=habit.description, active=habit.active)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

def update_habit(
    db: Session,
    habit_id: int,
    updated_data: schemas.HabitBase
):

    db_habit = get_habit(db, habit_id)

    if not db_habit:
        return None

    db_habit.name = updated_data.name
    db_habit.description = updated_data.description
    db_habit.active = updated_data.active

    db.commit()

    db.refresh(db_habit)

    return db_habit

def delete_habit(db: Session, habit_id: int):

    db_habit = get_habit(db, habit_id)

    if not db_habit:
        return None

    db.delete(db_habit)

    db.commit()

    return db_habit


def check_habit(db: Session, id_habits: int):

    existing_log = db.query(models.HabitLog).filter(
        models.HabitLog.id_habits == id_habits,
        models.HabitLog.done_date == date.today()
    ).first()

    if existing_log:
        return existing_log

    log = models.HabitLog(
        id_habits=id_habits,
        done_date=date.today()
    )

    db.add(log)

    db.commit()

    db.refresh(log)

    return log    

def get_logs_by_habit(
    db: Session,
    id_habits: int
):

    return db.query(models.HabitLog).filter(
        models.HabitLog.id_habits == id_habits
    ).all()