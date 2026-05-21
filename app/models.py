# Importações dos tipos de coluna do SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Date
# relationship: define relacionamentos entre tabelas (chave estrangeira)
from sqlalchemy.orm import relationship
# Base: classe pai de todos os modelos ORM do projeto
from .database import Base
# func: funções SQL nativas, usada aqui para o valor padrão de data (NOW())
from sqlalchemy.sql import func


# ─── Modelo: Habit ────────────────────────────────────────────────────────────
# Representa a tabela 'habits' no banco de dados.
# Cada linha é um hábito cadastrado pelo usuário.
class Habit(Base):
    __tablename__ = 'habits'

    # Chave primária gerada automaticamente pelo banco
    id = Column(Integer, primary_key=True, index=True)

    # Nome do hábito — obrigatório, máximo 255 caracteres
    name = Column(String(255), nullable=False)

    # Descrição opcional do hábito
    description = Column(Text)

    # Data/hora de criação — preenchida automaticamente pelo banco com NOW()
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Indica se o hábito está ativo (True) ou inativo (False)
    active = Column(Boolean, default=True, nullable=False)

    # Relacionamento 1-N com HabitLog:
    # - back_populates: espelho do relacionamento definido em HabitLog
    # - cascade="all, delete-orphan": ao deletar um hábito, todos os seus logs são deletados também
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")


# ─── Modelo: HabitLog ─────────────────────────────────────────────────────────
# Representa a tabela 'habits_logs' no banco de dados.
# Cada linha é um registro de check-in (hábito realizado em determinada data).
class HabitLog(Base):
    __tablename__ = 'habits_logs'

    # Chave primária gerada automaticamente
    id = Column(Integer, primary_key=True, index=True)

    # Chave estrangeira referenciando o hábito ao qual este log pertence
    id_habits = Column(Integer, ForeignKey('habits.id'), nullable=False)

    # Data em que o hábito foi realizado
    done_date = Column(Date, nullable=False)

    # Data/hora em que o registro foi criado — preenchida automaticamente pelo banco
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relacionamento N-1 com Habit: permite acessar habit.name a partir de um log
    habit = relationship("Habit", back_populates="logs")
