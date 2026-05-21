# Session: tipo da sessão do SQLAlchemy, usada para executar queries
from sqlalchemy.orm import Session
# models: modelos ORM (tabelas); schemas: schemas Pydantic (validação)
from app import models, schemas
# date: usado para registrar o check-in com a data de hoje
from datetime import date
from app.models import Habit


# ─── READ: buscar um hábito pelo ID ───────────────────────────────────────────
def get_habit(db: Session, habit_id: int):
    """Retorna o hábito com o ID informado, ou None se não existir."""
    return db.query(models.Habit).filter(models.Habit.id == habit_id).first()


# ─── READ: buscar todos os hábitos ────────────────────────────────────────────
def get_habits(db: Session):
    """Retorna a lista completa de hábitos cadastrados."""
    return db.query(models.Habit).all()


# ─── READ: buscar hábito por ID (alias de get_habit) ──────────────────────────
def get_habit_by_id(db: Session, habit_id: int):
    """Alias explícito de get_habit — retorna o hábito pelo ID."""
    return db.query(models.Habit).filter(models.Habit.id == habit_id).first()


# ─── CREATE: criar um novo hábito ─────────────────────────────────────────────
def create_habit(db: Session, habit: schemas.HabitBase):
    """Cria um novo hábito no banco a partir dos dados validados pelo schema."""
    # Instancia o modelo ORM com os dados recebidos
    db_habit = models.Habit(name=habit.name, description=habit.description, active=habit.active)

    db.add(db_habit)     # Adiciona o objeto à sessão (não persiste ainda)
    db.commit()          # Persiste no banco de dados
    db.refresh(db_habit) # Atualiza o objeto com os dados gerados pelo banco (ex: id, created_at)
    return db_habit


# ─── UPDATE: atualizar um hábito existente ────────────────────────────────────
def update_habit(
    db: Session,
    habit_id: int,
    updated_data: schemas.HabitBase
):
    """Atualiza name, description e active de um hábito. Retorna None se não encontrado."""
    db_habit = get_habit(db, habit_id)

    # Retorna None para que a rota possa responder com 404
    if not db_habit:
        return None

    # Aplica os novos valores no objeto ORM
    db_habit.name        = updated_data.name
    db_habit.description = updated_data.description
    db_habit.active      = updated_data.active

    db.commit()          # Persiste as alterações
    db.refresh(db_habit) # Sincroniza o objeto com o estado atual do banco
    return db_habit


# ─── DELETE: remover um hábito ────────────────────────────────────────────────
def delete_habit(db: Session, habit_id: int):
    """Remove o hábito e todos os seus logs (cascade). Retorna None se não encontrado."""
    db_habit = get_habit(db, habit_id)

    if not db_habit:
        return None

    db.delete(db_habit)  # Marca o objeto para exclusão (cascade apaga os logs também)
    db.commit()          # Confirma a exclusão no banco
    return db_habit      # Retorna o objeto deletado para confirmação na resposta


# ─── CHECK-IN: registrar hábito feito hoje ────────────────────────────────────
def check_habit(db: Session, id_habits: int):
    """
    Registra um check-in do hábito na data de hoje.
    Se já existe um log para hoje, retorna o existente (evita duplicatas).
    """
    # Verifica se já foi feito check-in hoje para este hábito
    existing_log = db.query(models.HabitLog).filter(
        models.HabitLog.id_habits == id_habits,
        models.HabitLog.done_date == date.today()
    ).first()

    # Se já existe, apenas retorna — sem criar duplicata
    if existing_log:
        return existing_log

    # Cria o novo registro de check-in com a data atual
    log = models.HabitLog(
        id_habits=id_habits,
        done_date=date.today()
    )

    db.add(log)
    db.commit()
    db.refresh(log)  # Atualiza o objeto com id e created_at gerados pelo banco
    return log


# ─── READ LOGS: buscar histórico de check-ins de um hábito ───────────────────
def get_logs_by_habit(
    db: Session,
    id_habits: int
):
    """Retorna todos os check-ins registrados para o hábito informado."""
    return db.query(models.HabitLog).filter(
        models.HabitLog.id_habits == id_habits
    ).all()