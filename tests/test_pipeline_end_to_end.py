import pytest
from unittest.mock import patch

from arcana.pipeline import ArcanaPipelineError, run_arcana_pipeline
from arcana.schema import ArcanaOutput


@patch("arcana.pipeline.run_granite")
def test_pipeline_end_to_end(
    mock_run_granite,
    moment_description: str,
    mock_granite_responses: list[str],
) -> None:
    mock_run_granite.side_effect = mock_granite_responses

    result = run_arcana_pipeline(moment_description)

    assert mock_run_granite.call_count == 3
    assert isinstance(result, ArcanaOutput)
    assert result.model_dump() == {
        "classification": {
            "moment_type": "The Trickster",
            "confidence": 0.91,
        },
        "card": {
            "card_name": "The Trickster",
            "card_id": "trickster",
            "reason": "The nutmeg and chaos align with trickster energy.",
        },
        "explanation": {
            "metaphor": "A pickpocket slips through the crowd unnoticed until the prize is gone.",
            "tactical_explanation": "A tight dribble in a congested box broke defensive shape and created the chance.",
            "cultural_context": "Moments like this echo street football's love of humiliating defenders.",
            "emotional_impact": "Supporters erupt with disbelief and delight at the audacity.",
        },
    }


@patch("arcana.pipeline.run_granite")
def test_pipeline_end_to_end_raises_on_parse_error(
    mock_run_granite,
    moment_description: str,
) -> None:
    mock_run_granite.return_value = "not valid json"

    with pytest.raises(ArcanaPipelineError) as exc_info:
        run_arcana_pipeline(moment_description)

    assert exc_info.value.stage == "classification"
    assert exc_info.value.raw_output == "not valid json"
    assert "Invalid JSON in Granite response" in exc_info.value.error_message
    assert mock_run_granite.call_count == 1
