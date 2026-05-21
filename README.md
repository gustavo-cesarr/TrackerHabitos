# TrackerHabitos

API REST + interface web para criação e monitoramento de hábitos diários, construída com **FastAPI**, **SQLAlchemy** e **PostgreSQL**.

---

## Sumário

- [Sobre](#sobre)
- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Rodando o projeto](#rodando-o-projeto)
- [Endpoints da API](#endpoints-da-api)
- [Interface Web](#interface-web)
- [Compartilhando externamente](#compartilhando-externamente)
- [Banco de dados](#banco-de-dados)

---

## Sobre

TrackerHabitos permite cadastrar hábitos, marcar check-ins diários e consultar o histórico de cada hábito. Possui tanto uma API REST documentada automaticamente (Swagger) quanto uma interface web responsiva que consome essa mesma API.

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend / API | [FastAPI](https://fastapi.tiangolo.com/) 0.136+ |
| Servidor ASGI | [Uvicorn](https://www.uvicorn.org/) |
| ORM | [SQLAlchemy](https://www.sqlalchemy.org/) 2.x |
| Banco de dados | [PostgreSQL](https://www.postgresql.org/) 18 |
| Driver PostgreSQL | psycopg2-binary |
| Templates HTML | Jinja2 |
| Variáveis de ambiente | python-dotenv |
| Gerenciador de ambiente | [uv](https://github.com/astral-sh/uv) |
| Frontend | HTML5 + CSS3 + JavaScript (Fetch API) |

---

## Estrutura do projeto

```
TrackerHabitos/
├── app/
│   ├── main.py        # Definição da aplicação FastAPI e rotas
│   ├── database.py    # Conexão com o banco e sessão SQLAlchemy
│   ├── models.py      # Modelos ORM (tabelas habits e habits_logs)
│   ├── schemas.py     # Schemas Pydantic (validação de entrada/saída)
│   └── crud.py        # Funções de acesso ao banco (Create/Read/Update/Delete)
├── template/
│   └── index.html     # Interface web principal
├── static/
│   └── style.css      # Estilos da interface
├── .env               # Variáveis de ambiente (não versionado)
├── .gitignore
└── requeriments.txt
```

---

## Pré-requisitos

- [Python 3.14+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv) (gerenciador de pacotes/ambientes)
- [PostgreSQL 18+](https://www.postgresql.org/download/) rodando localmente

> **Instalando o uv:**
> ```powershell
> winget install astral-sh.uv
> ```

---

## Instalação

```powershell
# 1. Clone o repositório
git clone https://github.com/seu-usuario/TrackerHabitos.git
cd TrackerHabitos

# 2. Crie o ambiente virtual e instale as dependências
uv venv .venv
.\.venv\Scripts\Activate.ps1
uv pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv jinja2
```

---

## Configuração

Crie um arquivo `.env` na raiz do projeto com a URL de conexão do PostgreSQL:

```env
DATABASE_URL=postgresql://USUARIO:SENHA@localhost:5432/NOME_DO_BANCO
```

**Exemplo:**
```env
DATABASE_URL=postgresql://postgres:minhasenha@localhost:5432/TrackerHabitos
```

> O banco de dados precisa existir previamente. Crie com:
> ```sql
> CREATE DATABASE "TrackerHabitos";
> ```
> As tabelas são criadas automaticamente pelo SQLAlchemy ao iniciar a aplicação.

---

## Rodando o projeto

```powershell
# Ative o ambiente virtual (se ainda não estiver ativo)
.\.venv\Scripts\Activate.ps1

# Inicie o servidor com hot-reload
uvicorn app.main:app --reload
```

Acesse em: **http://127.0.0.1:8000**

A documentação interativa da API (Swagger UI) está disponível em: **http://127.0.0.1:8000/docs**

---

## Endpoints da API

### Hábitos

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/habits` | Lista todos os hábitos |
| `GET` | `/habits/{id}` | Retorna um hábito pelo ID |
| `POST` | `/habits` | Cria um novo hábito |
| `PUT` | `/habits/{id}` | Atualiza um hábito existente |
| `DELETE` | `/habits/{id}` | Remove um hábito |

### Check-in e Logs

| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/habits/{id}/check` | Registra check-in do hábito na data de hoje |
| `GET` | `/habits/{id}/logs` | Lista todos os check-ins de um hábito |

### Exemplos de payload

**Criar/Atualizar hábito — `POST /habits` ou `PUT /habits/{id}`:**
```json
{
  "name": "Beber 2L de água",
  "description": "Manter hidratação ao longo do dia",
  "active": true
}
```

**Resposta:**
```json
{
  "id": 1,
  "name": "Beber 2L de água",
  "description": "Manter hidratação ao longo do dia",
  "active": true,
  "created_at": "2026-05-21T17:00:00"
}
```

---

## Interface Web

A interface web é servida pelo próprio FastAPI na rota `/` e consome a API via Fetch. Funcionalidades disponíveis:

- Listar todos os hábitos em cards
- Criar novo hábito (modal)
- Editar hábito existente (modal)
- Marcar hábito como feito no dia (check-in)
- Visualizar histórico de check-ins
- Excluir hábito
- Feedback visual com toast de sucesso/erro

---

## Compartilhando externamente

Para expor a aplicação local na internet sem deploy, use o **Cloudflare Tunnel**:

```powershell
# Instalar (necessário apenas uma vez)
winget install --id Cloudflare.cloudflared

# Com o uvicorn rodando, execute em outro terminal:
cloudflared tunnel --url http://localhost:8000
```

O comando gera um link público temporário no formato `https://xxxx.trycloudflare.com`.

---

## Banco de dados

### Modelo de dados

**Tabela `habits`**

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | INTEGER PK | Identificador único |
| `name` | VARCHAR(255) | Nome do hábito |
| `description` | TEXT | Descrição opcional |
| `active` | BOOLEAN | Se o hábito está ativo |
| `created_at` | DATETIME | Data de criação (automática) |

**Tabela `habits_logs`**

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | INTEGER PK | Identificador único |
| `id_habits` | INTEGER FK | Referência ao hábito |
| `done_date` | DATE | Data do check-in |
| `created_at` | DATETIME | Data do registro (automática) |

> Um check-in por hábito por dia — check-ins duplicados na mesma data retornam o registro existente.

