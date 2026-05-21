import os
# load_dotenv: carrega as variáveis do arquivo .env para os.environ
from dotenv import load_dotenv
# create_engine: cria a conexão principal com o banco de dados
from sqlalchemy import create_engine
# sessionmaker: fábrica de sessões para executar queries
# declarative_base: classe base da qual todos os modelos ORM herdam
from sqlalchemy.orm import sessionmaker, declarative_base

# Lê o arquivo .env na raiz do projeto e injeta as variáveis no ambiente
load_dotenv()

# Lê a URL de conexão do banco definida no .env
# Formato esperado: postgresql://usuario:senha@host:porta/nome_banco
DATABSE_URL = os.getenv('DATABASE_URL')

# Interrompe a inicialização imediatamente se a variável não estiver configurada
if not DATABSE_URL:
    raise ValueError("DATABASE_URL não encontrada no arquivo .env")

# Cria o engine — objeto central que gerencia o pool de conexões com o banco
engine = create_engine(DATABSE_URL)

# Fábrica de sessões:
# - autocommit=False: transações devem ser confirmadas manualmente com db.commit()
# - autoflush=False: evita envios automáticos de SQL antes do commit
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa: todos os modelos ORM do projeto herdam desta classe
# O SQLAlchemy usa ela para mapear as classes Python para as tabelas do banco
Base = declarative_base()


def get_db():
    """
    Gerador de sessão de banco de dados para injeção de dependência no FastAPI.

    Uso nas rotas:
        db: Session = Depends(get_db)

    Garante que a sessão seja sempre fechada ao final da requisição,
    mesmo que ocorra uma exceção durante o processamento.
    """
    db = SessionLocal()  # Abre uma nova sessão
    try:
        yield db         # Fornece a sessão para a rota que solicitou
    finally:
        db.close()       # Fecha a sessão ao final da requisição (com ou sem erro)