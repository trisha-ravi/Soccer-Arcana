import json

from arcana.prompts.explanation_prompt import (
    EXPLANATION_EXAMPLE,
    build_explanation_prompt,
)
from arcana.schema import ExplanationResult


def test_explanation_prompt(
    moment_description: str,
    trickster_metadata: dict[str, str],
) -> None:
    card_name = "The Trickster"
    prompt = build_explanation_prompt(moment_description, card_name, trickster_metadata)
    schema = ExplanationResult.model_json_schema()

    assert moment_description in prompt
    assert card_name in prompt
    assert json.dumps(trickster_metadata, indent=2) in prompt
    assert "Card metadata" in prompt

    assert '"metaphor"' in prompt
    assert '"tactical_explanation"' in prompt
    assert '"cultural_context"' in prompt
    assert '"emotional_impact"' in prompt
    assert "Example JSON object:" in prompt
    assert json.dumps(EXPLANATION_EXAMPLE, indent=2) in prompt
    assert "Do not include any extra text, commentary, or markdown" in prompt
    assert "Never include trailing commas" in prompt
    assert "Never wrap the JSON in backticks or code fences" in prompt
    assert json.dumps(schema, indent=2) in prompt
    assert prompt.strip().endswith(
        f"Return your answer ONLY as valid JSON matching this schema:\n{json.dumps(schema, indent=2)}"
    )
    ExplanationResult.model_validate(EXPLANATION_EXAMPLE)
