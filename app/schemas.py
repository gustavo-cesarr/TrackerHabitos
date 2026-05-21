# BaseModel: classe base do Pydantic para validação automática de dados
from pydantic import BaseModel
# Tipos de data usados nos schemas
from datetime import date, datetime
# Optional: indica que o campo pode ser None
from typing import Optional


# ─── Schema: HabitBase ────────────────────────────────────────────────────────
# Schema base com os campos que o USUÁRIO envia ao criar ou editar um hábito.
# Usado como corpo (body) nas rotas POST /habits e PUT /habits/{id}.
class HabitBase(BaseModel):
    # Nome do hábito — campo obrigatório
    name: str

    # Descrição do hábito — opcional, padrão None
    description: Optional[str] = None

    # Status do hábito — opcional, padrão True (ativo)
    active: Optional[bool] = True


# ─── Schema: HabitResponse ────────────────────────────────────────────────────
# Schema de RESPOSTA da API para hábitos.
# Herda os campos de HabitBase e adiciona os gerados pelo banco.
class HabitResponse(HabitBase):
    # ID gerado automaticamente pelo banco
    id: int
    name: str
    description: Optional[str] = None
    # Data de criação retornada pelo banco
    created_at: datetime

    class Config:
        # from_attributes=True permite converter objetos ORM (SQLAlchemy) diretamente para este schema
        model_config = {"from_attributes": True}


# ─── Schema: HabitLogCreate ───────────────────────────────────────────────────
# Schema com os dados necessários para registrar um check-in manualmente.
# Na prática, o endpoint POST /habits/{id}/check preenche esses dados automaticamente.
class HabitLogCreate(BaseModel):
    # ID do hábito ao qual o log pertence
    id_habits: int

    # Data em que o hábito foi realizado
    done_date: date


# ─── Schema: HabitLogResponse ─────────────────────────────────────────────────
# Schema de RESPOSTA da API para logs de check-in.
# Herda os campos de HabitLogCreate e adiciona os gerados pelo banco.
class HabitLogResponse(HabitLogCreate):
    # ID do log gerado pelo banco
    id: int
    id_habits: int
    done_date: date
    # Data/hora em que o registro foi criado no banco
    created_at: datetime

    class Config:
        # from_attributes=True permite converter objetos ORM diretamente para este schema
        model_config = {"from_attributes": True}