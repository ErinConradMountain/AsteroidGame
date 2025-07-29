"""Command-line interface for the Asteroid Game chatbot."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - hints only
    from openai import OpenAI as OpenAIClient
else:  # pragma: no cover - runtime import
    try:
        from openai import OpenAI as OpenAIClient
    except Exception:  # noqa: BLE001
        # Provide a fallback when the openai package is unavailable during testing.
        class OpenAIClient:  # type: ignore[too-few-public-methods]
            def __init__(self, *args, **kwargs) -> None:  # noqa: D401
                """Placeholder OpenAI client."""

        class chat:  # noqa: D401
            class completions:  # noqa: D401
                @staticmethod
                def create(*args, **kwargs):
                    return type(
                        "obj",
                        (),
                        {
                            "choices": [
                                type(
                                    "m",
                                    (),
                                    {"message": type("msg", (), {"content": ""})},
                                )
                            ]
                        },
                    )


from .knowledge_base import load_instructions


class AsteroidBot:
    """Chatbot that guides learners through building an asteroid game."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if self.api_key is None:
            raise ValueError("OPENROUTER_API_KEY must be provided")
        self.client = OpenAIClient(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        self.instructions = load_instructions()

    def ask(self, prompt: str) -> str:
        """Send a message to the model and return the reply."""
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                ],
            }
        ]
        completion = self.client.chat.completions.create(
            model="google/gemma-3-12b-it:free", messages=messages
        )
        return completion.choices[0].message.content

    def run(self) -> None:
        """Interact with the user via the terminal."""
        print("Welcome to the Asteroid Game helper!")
        for line in self.instructions:
            print(line)
        while True:
            user_input = input("\nAsk a question (or 'quit'): ")
            if user_input.lower() == "quit":
                break
            try:
                answer = self.ask(user_input)
            except Exception as exc:  # noqa: BLE001
                print(f"Error: {exc}")
                continue
            print(f"\nAssistant: {answer}")


def main() -> None:
    """Entry point for the chatbot."""
    bot = AsteroidBot()
    bot.run()


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
