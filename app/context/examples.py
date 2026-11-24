from pydantic import BaseModel


class EstimationExample(BaseModel):
    meeting_summary: str
    estimation: str


ESTIMATION_EXAMPLES: list[EstimationExample] = [
    EstimationExample(
        meeting_summary=(
            "El cliente necesita una plataforma web de gestión de inventario para un "
            "almacén mediano. Quiere stock en tiempo real, alertas de reposición, roles "
            "(admin, encargado y consulta), importación CSV y un panel con métricas. "
            "Ya tienen PostgreSQL en AWS. No hay aplicación móvil."
        ),
        estimation="""\
## Estimación: Plataforma de gestión de inventario

### Desglose de tareas:
1. Diseño UI/UX: 40 horas
2. Backend API (CRUD de inventario): 60 horas
3. Autenticación y roles: 20 horas
4. Alertas de reposición: 16 horas
5. Importación CSV: 14 horas
6. Panel de métricas: 30 horas
7. Integración con PostgreSQL en AWS: 10 horas
8. Testing y QA: 25 horas

**Total estimado: 215 horas**
**Equipo recomendado: 2 desarrolladores full-stack + 1 diseñador UX (part-time)**
**Duración estimada: 8-10 semanas**
""",
    ),
    EstimationExample(
        meeting_summary=(
            "Una inmobiliaria quiere una landing para captar leads de viviendas. "
            "El diseño ya está en Figma. Necesitan formulario de contacto, envío de "
            "leads a HubSpot y una galería filtrable. El plazo orientativo es de un mes. "
            "No hay área privada ni pasarela de pago."
        ),
        estimation="""\
## Estimación: Landing inmobiliaria con HubSpot

### Desglose de tareas:
1. Adaptación del diseño de Figma: 16 horas
2. Maquetación responsive de la landing: 24 horas
3. Formulario de contacto con validación: 10 horas
4. Integración con HubSpot: 14 horas
5. Galería con filtros: 16 horas
6. Testing y ajustes: 12 horas
7. Despliegue: 4 horas

**Total estimado: 96 horas**
**Equipo recomendado: 1 desarrollador frontend + 1 diseñador UX (part-time, primera semana)**
**Duración estimada: 4-5 semanas**
""",
    ),
]
