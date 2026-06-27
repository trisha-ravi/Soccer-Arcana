import json
from typing import Any

from arcana.prompts.json_output import build_json_output_section
from arcana.schema import ExplanationResult

EXPLANATION_EXAMPLE = {
    "metaphor": "A fox slips through the henhouse unnoticed.",
    "tactical_explanation": "A dribble in tight space broke the defensive line.",
    "cultural_context": "Street football culture celebrates humiliating defenders.",
    "emotional_impact": "Supporters gasp, then erupt in delight.",
}


def build_explanation_prompt(
    moment_description: str,
    card_name: str,
    card_metadata: dict[str, Any],
) -> str:
    """Build a prompt that asks Granite to generate a full Arcana explanation."""
    card_metadata_json = json.dumps(card_metadata, indent=2)
    json_output_section = build_json_output_section(
        ExplanationResult, EXPLANATION_EXAMPLE
    )

    return f"""You are Soccer Arcana, an explainable AI that interprets soccer match moments through symbolic Arcana cards.

Match moment:
{moment_description}

Selected card: {card_name}

Card metadata:
{card_metadata_json}

Generate a complete Arcana reading for this moment using the selected card. Draw on the card's symbolic, tactical, emotional, and cultural meanings while grounding the reading in the specific match moment.

Rules:
- "metaphor" should be a vivid, accessible metaphor for what this moment means in the story of the match.
- "tactical_explanation" should clearly explain the on-pitch tactics in simple terms for soccer fans.
- "cultural_context" should connect the moment to broader soccer culture, tradition, or narrative context.
- "emotional_impact" should capture how this moment would feel to players and supporters.
- Keep each field concise (two to four sentences).

{json_output_section}"""
