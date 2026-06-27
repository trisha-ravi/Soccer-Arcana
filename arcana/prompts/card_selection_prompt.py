import json

from arcana.cards import ARCANA_CARDS
from arcana.prompts.json_output import build_json_output_section
from arcana.schema import CardSelectionResult

CARD_SELECTION_EXAMPLE = {
    "card_name": "The Trickster",
    "reason": "The moment's flair and deception align with this card.",
}


def build_card_selection_prompt(classification: str) -> str:
    """Build a prompt that asks Granite to select the best Arcana card for a classification."""
    cards_json = json.dumps(ARCANA_CARDS, indent=2)
    json_output_section = build_json_output_section(
        CardSelectionResult, CARD_SELECTION_EXAMPLE
    )

    return f"""You are Soccer Arcana, an explainable AI that selects the most fitting symbolic card for a classified match moment.

Classification:
{classification}

Arcana deck (choose exactly one card):
{cards_json}

Select the single Arcana card that best matches this classification. Consider each card's symbolic, tactical, emotional, and cultural meanings.

Rules:
- "card_name" must be exactly one of the card names from the Arcana deck.
- "reason" must be a concise explanation (one or two sentences).

{json_output_section}"""
