from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Habit Tracker API",
    description="API simples para controle de hábitos",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Habit Tracker API está rodando"}


@app.get("/habits", response_model=list[schemas.HabitResponse])
def list_habits(db: Session = Depends(get_db)):
    return crud.get_habits(db)


@app.get("/habits/{habit_id}", response_model=schemas.HabitResponse)
def get_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = crud.get_habit(db, habit_id)

    if not habit:
        raise HTTPException(status_code=404, detail="Hábito não encontrado")

    return habit


@app.post("/habits", response_model=schemas.HabitResponse)
def create_habit(habit: schemas.HabitBase, db: Session = Depends(get_db)):
    return crud.create_habit(db, habit)


@app.put("/habits/{habit_id}", response_model=schemas.HabitResponse)
def update_habit(
    habit_id: int,
    habit: schemas.HabitBase,
    db: Session = Depends(get_db)
):
    updated_habit = crud.update_habit(db, habit_id, habit)

    if not updated_habit:
        raise HTTPException(status_code=404, detail="Hábito não encontrado")

    return updated_habit


@app.delete("/habits/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    deleted_habit = crud.delete_habit(db, habit_id)

    if not deleted_habit:
        raise HTTPException(status_code=404, detail="Hábito não encontrado")

    return {"message": "Hábito deletado com sucesso"}


@app.post("/habits/{habit_id}/check", response_model=schemas.HabitLogResponse)
def check_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = crud.get_habit(db, habit_id)

    if not habit:
        raise HTTPException(status_code=404, detail="Hábito não encontrado")

    return crud.check_habit(db, habit_id)


@app.get("/habits/{habit_id}/logs", response_model=list[schemas.HabitLogResponse])
def get_habit_logs(habit_id: int, db: Session = Depends(get_db)):
    habit = crud.get_habit(db, habit_id)

    if not habit:
        raise HTTPException(status_code=404, detail="Hábito não encontrado")

    return crud.get_logs_by_habit(db, habit_id)
