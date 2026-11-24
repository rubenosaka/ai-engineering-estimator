# Contexto del programa

Este repositorio es el Proyecto 1 del máster de AI Engineering con Lidr: el servicio que estima software a partir de una transcripción, con arquitectura CAG. El enunciado está en [ejercicio.md](ejercicio.md).

El diario del curso y las decisiones de entorno viven en la página de Notion [AI Engineering - Master](https://app.notion.com/p/4198bf383375800f9416ebbba1efc54f). El repositorio hermano, en `C:\rga\ai-engineering-lidr` ([rubenosaka/ai-engineering-lidr](https://github.com/rubenosaka/ai-engineering-lidr)), guarda el servicio base del programa, la sesión 01 y las decisiones de arquitectura. Lo que sigue sale de su `README.md`, `AGENTS.md`, `docs/arquitectura.md` y de esa página, leídos el 24 de noviembre de 2026.

## Qué es cada repositorio

| Repositorio | Papel |
| --- | --- |
| `ai-engineering-lidr` | Servicio base del máster. Salud, completions y la primera llamada a un LLM. PostgreSQL con imagen pgvector, todavía sin esquema. |
| `ai-engineering-estimator` | Caso de uso de estimación. Contexto estático en el prompt, sin base de datos ni retrieval. |

El programa empezó el 17 de noviembre de 2026. La API en Python queda separada del frontal. Streamlit, Chainlit, React o Rails solo consumen esa API. En producción el frontal no será un framework de prototipo. Hasta confirmarlo con el tutor, el frontal de trabajo previsto es Streamlit, y entra en el ejercicio previo a la sesión 3. Hoy no está en ninguno de los dos repositorios.

## Lo que ya está hecho en el otro proyecto

Comprobado en local el 15 de noviembre de 2026:

- Python del proyecto fijado en 3.12 con uv. El `python` del sistema es 3.14 y no es el intérprete del proyecto. `uv` 0.13.8 está en el PATH.
- FastAPI con `GET /health` (`{"status":"ok"}`) y OpenAPI en `/docs`.
- `POST /completions` elige el proveedor por el prefijo del modelo: `openai/gpt-5.4-mini` o `anthropic/claude-sonnet-4-6`.
- Las llamadas pasan por el puerto `LanguageModel`. El adaptador es LiteLLM (`LiteLLMLanguageModel`). La ruta no instancia el SDK de un proveedor.
- Sesión 01 resuelta en `exercises/session_01/first_call.py`. El enunciado original está en `exercises/session_01/sesion_01_ejercicios_alumno.py`. Niveles 1 y 2 obligatorios (llamada básica y system prompt); nivel 3 opcional (tokens y coste). Modelos de esa sesión: `openai/gpt-4o-mini` y `anthropic/claude-haiku-4-5-20251001`. Se ejecuta con `uv run python -m exercises.session_01.first_call` y no forma parte de los tests.
- Docker Compose levanta la API en el puerto 8000 y PostgreSQL en el 5432. Las credenciales salen de `.env`. La API todavía no abre conexiones a la base.
- Secretos solo en `.env`. Ese archivo no se versiona, no entra en la imagen y `.env.example` solo publica nombres vacíos.
- SDKs instalados sin llamadas de arranque: OpenAI 3.51.0, Anthropic 2.8.0, LiteLLM 1.109.1.

La regla de partición en ese repositorio es no crear carpetas de dominio vacías. Cuando existe un caso de uso, el código se separa en API, casos de uso, adaptadores e interfaz. El caso de uso de estimación es este repositorio.

## Cómo se aplica aquí

La estructura pedida por el enunciado ya está en `app/`: `routers/` para HTTP, `services/` para la llamada al modelo y `context/` para los ejemplos estáticos. Hay además `app/schemas/` para los contratos Pydantic, tests de salud y un Compose propio para ejecutar el servicio sin instalar Python en el host.

Diferencias conscientes respecto al otro proyecto:

- El enunciado pide Python 3.11 o superior. Este repositorio fija 3.11 en `.python-version` y `requires-python = ">=3.11"`. Lidr solo acepta 3.12.
- Allí el proveedor sale del prefijo del modelo y el único adaptador es LiteLLM. Aquí `LLM_PROVIDER` elige OpenAI o Anthropic y `llm_service.py` llama al SDK correspondiente. El enunciado de este ejercicio lo permite.
- Los ejemplos de `app/context/examples.py` son tres (inventario, landing inmobiliaria con HubSpot y SaaS de suscripciones), por encima del mínimo de dos.
- La respuesta de `POST /api/v1/estimate` añade `usage` (tokens de entrada, salida y total) a los campos `estimation`, `model` y `provider`.
- `GET /health` devuelve `status`, `version` y `environment`. En Lidr solo devuelve `status`.
- No hay PostgreSQL. En CAG el contexto viaja en el prompt. La base con pgvector queda para la evolución a RAG.

Modelos de referencia del programa, todavía no usados por este servicio: GPT-5.4, GPT-5.4 mini y GPT-5.4 nano; Claude Sonnet 4.6, Opus 4.6 y Haiku 4.5; embeddings `text-embedding-3-small` y `text-embedding-3-large`. Sentence Transformers entra en la sesión 7.

## Siguiente paso, todavía sin hacer

Queda definido como intención, no como trabajo hecho:

- Un pipeline que compruebe de forma automática que la estructura de carpetas es la del enunciado y que el servicio responde.
- Un repositorio de alumno con el README y la transcripción de reunión que se usará como cuerpo de `POST /api/v1/estimate`.
- Este repositorio como proyecto resuelto, para quien se atasque en el setup.
