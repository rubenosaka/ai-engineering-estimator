from app.context.examples import EstimationExample


def build_system_prompt(examples: list[EstimationExample]) -> str:
    blocks: list[str] = []
    for index, example in enumerate(examples, start=1):
        blocks.append(
            f"--- Ejemplo {index} ---\n"
            f"Resumen de la reunión:\n{example.meeting_summary}\n\n"
            f"Estimación:\n{example.estimation.strip()}"
        )
    examples_text = "\n\n".join(blocks)
    return (
        "Eres un estimador de software senior. Generas una estimación a partir de la "
        "transcripción de una reunión y de estimaciones previas que recibes como referencia.\n\n"
        "Responde en el idioma de la transcripción. Sigue la estructura de los ejemplos: "
        "título, desglose de tareas con horas, total, equipo recomendado y duración.\n\n"
        f"{examples_text}"
    )
