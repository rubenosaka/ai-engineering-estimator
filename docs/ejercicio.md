# Proyecto 1 — Estimación de software con arquitectura CAG

Enunciado del ejercicio del máster de AI Engineering. Este repositorio es una implementación de esa estructura.

## Objetivo

Construir la estructura base del Proyecto 1: una aplicación FastAPI con un endpoint que reciba el texto de una transcripción de reunión y devuelva una estimación de software generada por un LLM, utilizando arquitectura CAG (contexto estático inyectado en el prompt).

Al finalizar el ejercicio, el servicio:

- Recibe una transcripción de reunión vía API REST.
- Inyecta contexto estático (ejemplos de estimaciones previas) directamente en el prompt.
- Envía la petición a un LLM (OpenAI o Anthropic).
- Devuelve la estimación generada como respuesta JSON.

## Contexto del proyecto

Este es el inicio del proyecto que se ejecuta a lo largo del programa.

La arquitectura inicial es CAG: todo el contexto que necesita el modelo viaja en cada llamada. No hay base de datos, no hay retrieval y no hay persistencia.

Los datos de referencia (unas pocas estimaciones de ejemplo) caben en la ventana de contexto del modelo. No hace falta infraestructura adicional. Esa simplicidad permite centrarse en la lógica de negocio y en la calidad del prompt antes de evolucionar hacia RAG en módulos posteriores.

## Requisitos

- Python 3.11 o superior.
- [uv](https://docs.astral.sh/uv/) como gestor de paquetes.
- Cuenta activa en OpenAI Platform y/o Anthropic Console, con créditos (configurada en la sesión 01).
- API key disponible como variable de entorno.

## Paso 1 — Inicializar el proyecto

Crear el proyecto y configurarlo con uv:

```text
estimador-cag/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── estimations.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── llm_service.py
│   └── context/
│       ├── __init__.py
│       └── examples.py
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

Dependencias:

- `fastapi`
- `uvicorn[standard]`
- `pydantic-settings`
- `openai` y/o `anthropic`, según el proveedor
- `python-dotenv`

`routers/` gestiona los endpoints HTTP, `services/` contiene la llamada al LLM y `context/` guarda los datos estáticos que se inyectan en el prompt. La separación no es necesaria para que funcione; sí lo es para que el servicio escale.

## Paso 2 — Configuración con variables de entorno

`config.py` carga la configuración con Pydantic `BaseSettings` desde `.env`.

El enunciado original mostraba la lista en una captura. Las variables que usa este servicio, documentadas en `.env.example`, son:

| Variable | Uso |
| --- | --- |
| `OPENAI_API_KEY` | Clave de OpenAI. Vacía si no se usa ese proveedor. |
| `ANTHROPIC_API_KEY` | Clave de Anthropic. Vacía si no se usa ese proveedor. |
| `LLM_PROVIDER` | `openai` o `anthropic`. |
| `LLM_MODEL` | Modelo económico: `gpt-4o-mini` o el equivalente de Haiku. |
| `APP_ENV` | `development`, `staging` o `production`. |
| `LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING` o `ERROR`. |

`.env` lleva los valores reales y está en `.gitignore`. `.env.example` documenta los nombres sin valores.

## Paso 3 — Datos de contexto estático

En `context/examples.py`, definir al menos dos ejemplos de estimaciones previas. Esos ejemplos son el conocimiento del sistema: las estimaciones históricas que el modelo usa como referencia.

Cada ejemplo incluye:

- Un resumen de la transcripción original: qué pedía el cliente.
- La estimación generada: desglose de tareas con horas y costes.

Estructura orientativa:

```python
ESTIMATION_EXAMPLES = [
    {
        "meeting_summary": "El cliente necesita una plataforma web de gestión de inventario...",
        "estimation": """
        ## Estimación: Plataforma de Gestión de Inventario

        ### Desglose de tareas:
        1. Diseño UI/UX: 40 horas
        2. Backend API (CRUD inventario): 60 horas
        3. Autenticación y roles: 20 horas
        4. Dashboard con métricas: 30 horas
        5. Testing y QA: 25 horas

        **Total estimado: 175 horas**
        **Equipo recomendado: 2 desarrolladores full-stack + 1 diseñador UX (part-time)**
        **Duración estimada: 6-8 semanas**
        """,
    },
]
```

Funcionan como few-shot examples. Cuanto más representativos sean del tipo de estimación que se quiere generar, mejor será la salida.

## Paso 4 — Servicio de llamada al LLM

En `services/llm_service.py`, una función que:

1. Construye el system prompt. El modelo es un estimador de software experto que genera estimaciones a partir de ejemplos previos y de la transcripción de una reunión nueva.
2. Inyecta los ejemplos del paso 3 en el prompt. El contexto viaja en la llamada: eso es CAG.
3. Envía la transcripción como mensaje de usuario.
4. Devuelve la estimación generada.

Patrón de mensajes:

```text
[system]    → Instrucciones + ejemplos de estimaciones previas
[user]      → Transcripción de la reunión a estimar
[assistant] → Estimación generada
```

Implementar al menos un proveedor (OpenAI o Anthropic). Si se implementan ambos, `LLM_PROVIDER` elige cuál usar.

Modelos económicos de este ejercicio: `gpt-4o-mini` en OpenAI o `claude-haiku-4-5` en Anthropic.

## Paso 5 — Endpoint de estimación

En `routers/estimations.py`, `POST /api/v1/estimate`:

- Recibe un JSON con al menos el campo `transcription`.
- Llama al servicio del paso 4.
- Devuelve la estimación en JSON.

Request:

```json
{
  "transcription": "En la reunión con el cliente se discutió la necesidad de..."
}
```

Response:

```json
{
  "estimation": "## Estimación: ...\n\n### Desglose de tareas:\n...",
  "model": "gpt-4o-mini",
  "provider": "openai"
}
```

Se pueden añadir campos útiles: tokens utilizados, coste estimado, timestamp.

## Paso 6 — Aplicación FastAPI

En `main.py`:

- Incluir el router de estimaciones con el prefijo `/api/v1`.
- Añadir `GET /health` con el estado del servicio.
- Configurar título y descripción para la documentación automática (Swagger en `/docs`).

## Paso 7 — Verificación

```bash
uv run uvicorn app.main:app --reload
```

En otra terminal:

```bash
curl -X POST http://localhost:8000/api/v1/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "transcription": "En la reunión con el equipo de marketing, el cliente explicó que necesita una landing page con formulario de contacto, integración con su CRM actual (HubSpot), y una sección de blog con editor WYSIWYG. El plazo ideal sería tenerlo listo en 4 semanas. El diseño ya existe en Figma."
  }'
```

También se puede probar desde Swagger UI en `http://localhost:8000/docs`.

## Checklist

- [ ] El proyecto arranca sin errores con `uv run uvicorn app.main:app --reload`.
- [ ] Las API keys se cargan desde `.env` y no aparecen en el código.
- [ ] `GET /health` responde con status 200.
- [ ] `POST /api/v1/estimate` recibe una transcripción y devuelve una estimación.
- [ ] La estimación se inspira en los ejemplos de contexto inyectados.
- [ ] La documentación Swagger está accesible en `/docs`.
- [ ] `.env` está en `.gitignore`.

## Entregable

Proyecto funcional con la estructura descrita, capaz de recibir una transcripción y devolver una estimación generada por un LLM con arquitectura CAG.

La calidad de las estimaciones no tiene que ser perfecta en este punto. Se itera en la sesión en vivo. Lo que importa es el flujo completo: recibir texto, inyectar contexto, llamar al LLM y devolver la respuesta.

## Sesión en vivo

En la sesión en vivo se trabaja sobre este scaffolding para:

- Resolver problemas comunes del setup.
- Iterar la arquitectura CAG: mejorar los ejemplos, optimizar el prompt, analizar la calidad de las estimaciones y explorar los parámetros del modelo.

Hay que llegar con el proyecto funcionando. El tiempo de la sesión se dedica a la calidad, no al setup.
