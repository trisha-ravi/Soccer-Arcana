import json

import pytest

from arcana.cards import ARCANA_CARDS


@pytest.fixture
def moment_description() -> str:
    return "A nutmeg in the box leads to a scrambled equalizer."


@pytest.fixture
def classification_json() -> str:
    return json.dumps(
        {
            "moment_type": "The Trickster",
            "confidence": 0.91,
        }
    )


@pytest.fixture
def card_selection_json() -> str:
    return json.dumps(
        {
            "card_name": "The Trickster",
            "reason": "The nutmeg and chaos align with trickster energy.",
        }
    )


@pytest.fixture
def explanation_json() -> str:
    return json.dumps(
        {
            "metaphor": "A pickpocket slips through the crowd unnoticed until the prize is gone.",
            "tactical_explanation": "A tight dribble in a congested box broke defensive shape and created the chance.",
            "cultural_context": "Moments like this echo street football's love of humiliating defenders.",
            "emotional_impact": "Supporters erupt with disbelief and delight at the audacity.",
        }
    )


@pytest.fixture
def mock_granite_responses(
    classification_json: str,
    card_selection_json: str,
    explanation_json: str,
) -> list[str]:
    return [classification_json, card_selection_json, explanation_json]


@pytest.fixture
def trickster_metadata() -> dict[str, str]:
    return ARCANA_CARDS["The Trickster"]
