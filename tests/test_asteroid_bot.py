import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
"""Tests for the asteroid bot."""
from src.asteroid_bot import AsteroidBot  # noqa: E402


def test_load_instructions() -> None:
    bot = AsteroidBot(api_key="test")
    assert bot.instructions


def test_ask(monkeypatch) -> None:
    class DummyClient:
        def __init__(self, *args, **kwargs) -> None:
            pass

        class chat:
            class completions:
                @staticmethod
                def create(model: str, messages):  # type: ignore[no-redef]
                    return type(
                        "obj",
                        (),
                        {
                            "choices": [
                                type(
                                    "m",
                                    (),
                                    {"message": type("msg", (), {"content": "ok"})},
                                )
                            ]
                        },
                    )

    monkeypatch.setattr("src.asteroid_bot.OpenAIClient", DummyClient)
    bot = AsteroidBot(api_key="test")
    assert bot.ask("hi") == "ok"
