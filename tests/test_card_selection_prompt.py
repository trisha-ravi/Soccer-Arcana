import json

from arcana.cards import ARCANA_CARDS
from arcana.prompts.card_selection_prompt import (
    CARD_SELECTION_EXAMPLE,
    build_card_selection_prompt,
)
from arcana.schema import CardSelectionResult


def test_card_selection_prompt(classification_json: str) -> None:
    prompt = build_card_selection_prompt(classification_json)
    schema = CardSelectionResult.model_json_schema()

    assert classification_json in prompt
    assert "You are Soccer Arcana" in prompt
    assert "Arcana deck" in prompt

    for card_name in ARCANA_CARDS:
        assert card_name in prompt

    assert '"symbolic_meaning"' in prompt
    assert '"tactical_meaning"' in prompt
    assert '"emotional_meaning"' in prompt
    assert '"cultural_meaning"' in prompt

    assert '"card_name"' in prompt
    assert '"reason"' in prompt
    assert "Example JSON object:" in prompt
    assert json.dumps(CARD_SELECTION_EXAMPLE, indent=2) in prompt
    assert "Do not include any extra text, commentary, or markdown" in prompt
    assert "Never include trailing commas" in prompt
    assert "Never wrap the JSON in backticks or code fences" in prompt
    assert json.dumps(schema, indent=2) in prompt
    assert prompt.strip().endswith(
        f"Return your answer ONLY as valid JSON matching this schema:\n{json.dumps(schema, indent=2)}"
    )
    CardSelectionResult.model_validate(CARD_SELECTION_EXAMPLE)
