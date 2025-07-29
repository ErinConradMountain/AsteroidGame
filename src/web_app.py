"""Flask web interface for the Asteroid Bot."""

from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from .asteroid_bot import AsteroidBot


def create_app(api_key: str | None = None) -> Flask:
    """Create and configure the Flask application.

    Args:
        api_key: Optional API key for the chatbot.

    Returns:
        Flask: Configured Flask application.
    """

    bot = AsteroidBot(api_key=api_key)
    app = Flask(__name__)

    @app.route("/")
    def index() -> str:
        """Render the chat page."""

        return render_template("index.html")

    @app.route("/ask", methods=["POST"])
    def ask() -> "tuple[str, int]":
        """Return an answer from the chatbot."""

        prompt = request.form.get("prompt", "")
        if not prompt:
            return jsonify({"answer": "No prompt provided."}), 400
        # Image data is currently ignored but stored for future use
        if request.files.get("image"):
            request.files["image"].read()  # pragma: no cover - placeholder
        answer = bot.ask(prompt)
        return jsonify({"answer": answer}), 200

    return app


def main() -> None:
    """Run the web application."""

    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
