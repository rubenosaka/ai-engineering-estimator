# Estimador CAG

Servicio FastAPI que recibe la transcripción de una reunión y devuelve una estimación de software. Los ejemplos de referencia van en el prompt de cada llamada. No hay base de datos ni retrieval.

El enunciado está en [exercice.md](exercice.md). La carpeta `solved/` es una referencia aparte y no forma parte de este servicio.

## Requisitos

- Python 3.12, gestionado por [uv](https://docs.astral.sh/uv/)
- Docker, si se arranca con Compose
- Una API key de OpenAI o de Anthropic

## Arranque local

```powershell
uv sync
copy .env.example .env
uv run uvicorn app.main:app --reload
```

Rellena en `.env` la clave del proveedor indicado por `LLM_PROVIDER`.

- OpenAI: `LLM_PROVIDER=openai` y `LLM_MODEL=gpt-4o-mini`
- Anthropic: `LLM_PROVIDER=anthropic` y `LLM_MODEL=claude-haiku-4-5`

- Salud: http://localhost:8000/health
- Swagger: http://localhost:8000/docs
- Estimación: `POST /api/v1/estimate` con `{"transcription": "..."}`

## Docker

```powershell
docker compose up --build
```

`.env` no entra en la imagen. Compose lo inyecta al arrancar el contenedor.

## Pruebas

```powershell
uv run pytest
```

Las pruebas del endpoint usan un modelo falso. No llaman a OpenAI ni a Anthropic.
