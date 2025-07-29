"""Knowledge base for the asteroid game assistant.

Learner Note: This is the expected format. Each module should start with
a docstring explaining its purpose in plain language.
"""

from pathlib import Path
from typing import List


BASE_PATH = Path(__file__).resolve().parent.parent / "knowledge_base"


def load_instructions() -> List[str]:
    """Load game-building instructions from the knowledge base.

    Returns:
        List[str]: Lines of instructions.
    """
    file_path = BASE_PATH / "instructions.txt"
    if not file_path.exists():
        return [
            "Instructions will be provided soon.",
            "Please check back later.",
        ]
    return file_path.read_text().splitlines()
