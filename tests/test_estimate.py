from fastapi.testclient import TestClient

from app.main import app, get_language_model
from app.services.llm import ChatMessage, Completion, LanguageModelError, TokenUsage

TRANSCRIPTION = (
    "En la reunión el cliente pidió una landing con formulario, HubSpot y un blog. "
    "El diseño está en Figma y el plazo es de cuatro semanas."
)


class FakeLanguageModel:
    def __init__(self) -> None:
        self.messages: list[ChatMessage] = []

    def complete(self, messages: list[ChatMessage]) -> Completion:
        self.messages = messages
        return Completion(
            content="## Estimación: Landing con HubSpot\n\n**Total estimado: 90 horas**",
            model="fake-model",
            provider="openai",
            usage=TokenUsage(input_tokens=12, output_tokens=8, total_tokens=20),
        )


def test_estimate_returns_the_model_response(client: TestClient) -> None:
    fake = FakeLanguageModel()
    app.dependency_overrides[get_language_model] = lambda: fake

    response = client.post("/api/v1/estimate", json={"transcription": TRANSCRIPTION})

    assert response.status_code == 200
    assert response.json() == {
        "estimation": "## Estimación: Landing con HubSpot\n\n**Total estimado: 90 horas**",
        "model": "fake-model",
        "provider": "openai",
        "usage": {"input_tokens": 12, "output_tokens": 8, "total_tokens": 20},
    }
    assert fake.messages[0].role == "system"
    assert "Plataforma de gestión de inventario" in fake.messages[0].content
    assert "Landing inmobiliaria con HubSpot" in fake.messages[0].content
    assert fake.messages[1] == ChatMessage(role="user", content=TRANSCRIPTION)


def test_estimate_rejects_an_empty_transcription(client: TestClient) -> None:
    app.dependency_overrides[get_language_model] = lambda: FakeLanguageModel()

    response = client.post("/api/v1/estimate", json={"transcription": ""})

    assert response.status_code == 422


def test_estimate_hides_provider_errors(client: TestClient) -> None:
    class FailingLanguageModel:
        def complete(self, messages: list[ChatMessage]) -> Completion:
            raise LanguageModelError("secret sk-test should not leak")

    app.dependency_overrides[get_language_model] = lambda: FailingLanguageModel()

    response = client.post("/api/v1/estimate", json={"transcription": TRANSCRIPTION})

    assert response.status_code == 500
    assert response.json()["detail"] == "Estimation failed"
    assert "sk-test" not in response.text
