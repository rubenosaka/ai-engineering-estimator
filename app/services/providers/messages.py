from app.services.llm import ChatMessage


def to_openai_messages(messages: list[ChatMessage]) -> list[dict[str, str]]:
    return [{"role": message.role, "content": message.content} for message in messages]


def to_anthropic_messages(messages: list[ChatMessage]) -> tuple[str, list[dict[str, str]]]:
    system = "\n\n".join(message.content for message in messages if message.role == "system")
    dialogue = [
        {"role": message.role, "content": message.content}
        for message in messages
        if message.role != "system"
    ]
    return system, dialogue
