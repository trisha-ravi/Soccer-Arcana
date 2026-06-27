import json

from arcana.cards import ARCANA_CARDS
from arcana.prompts.json_output import build_json_output_section
from arcana.schema import ClassificationResult

CLASSIFICATION_CATEGORIES = list(ARCANA_CARDS.keys())

CLASSIFICATION_EXAMPLE = {
    "moment_type": "The Trickster",
    "confidence": 0.85,
}


def build_classification_prompt(moment_description: str) -> str:
    """Build a prompt that asks Granite to classify a moment into an Arcana card."""
    categories_json = json.dumps(CLASSIFICATION_CATEGORIES, indent=2)
    json_output_section = build_json_output_section(
        ClassificationResult, CLASSIFICATION_EXAMPLE
    )

    return f"""You are Soccer Arcana, an explainable AI that classifies soccer match moments into symbolic card categories.

Match moment:
{moment_description}

Predefined categories (choose exactly one):
{categories_json}

Classify this moment into the single best-fitting category from the list above.

Rules:
- "moment_type" must be exactly one of the predefined category names.
- "confidence" must be a number between 0 and 1.

{json_output_section}"""
