import json

from arcana.cards import ARCANA_CARDS
from arcana.prompts.classification_prompt import (
    CLASSIFICATION_CATEGORIES,
    CLASSIFICATION_EXAMPLE,
    build_classification_prompt,
)
from arcana.schema import ClassificationResult


def test_classification_prompt(moment_description: str) -> None:
    prompt = build_classification_prompt(moment_description)
    schema = ClassificationResult.model_json_schema()

    assert moment_description in prompt
    assert "You are Soccer Arcana" in prompt
    assert "Predefined categories" in prompt

    for category in CLASSIFICATION_CATEGORIES:
        assert category in prompt

    for card_name in ARCANA_CARDS:
        assert card_name in prompt

    assert '"moment_type"' in prompt
    assert '"confidence"' in prompt
    assert "Example JSON object:" in prompt
    assert json.dumps(CLASSIFICATION_EXAMPLE, indent=2) in prompt
    assert "Do not include any extra text, commentary, or markdown" in prompt
    assert "Never include trailing commas" in prompt
    assert "Never wrap the JSON in backticks or code fences" in prompt
    assert json.dumps(schema, indent=2) in prompt
    assert prompt.strip().endswith(
        f"Return your answer ONLY as valid JSON matching this schema:\n{json.dumps(schema, indent=2)}"
    )
    ClassificationResult.model_validate(CLASSIFICATION_EXAMPLE)
