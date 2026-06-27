import json

from pydantic import BaseModel, ValidationError

from arcana.cards import ARCANA_CARDS, CARD_IDS
from arcana.llm_engine import run_granite
from arcana.prompts.card_selection_prompt import build_card_selection_prompt
from arcana.prompts.classification_prompt import build_classification_prompt
from arcana.prompts.explanation_prompt import build_explanation_prompt
from arcana.schema import (
    ArcanaOutput,
    CardSelectionResult,
    ClassificationResult,
    ExplanationResult,
    ResolvedCardSelection,
)


class ArcanaPipelineError(Exception):
    def __init__(self, stage: str, raw_output: str, error_message: str) -> None:
        self.stage = stage
        self.raw_output = raw_output
        self.error_message = error_message
        super().__init__(error_message)


def _parse_and_validate(
    raw_output: str,
    model: type[BaseModel],
    stage: str,
) -> BaseModel:
    try:
        data = json.loads(raw_output.strip())
    except json.JSONDecodeError as exc:
        raise ArcanaPipelineError(
            stage=stage,
            raw_output=raw_output,
            error_message=f"Invalid JSON in Granite response: {exc}",
        ) from exc

    try:
        return model.model_validate(data)
    except ValidationError as exc:
        raise ArcanaPipelineError(
            stage=stage,
            raw_output=raw_output,
            error_message=f"Granite response does not match expected schema: {exc}",
        ) from exc


def run_arcana_pipeline(moment_description: str) -> ArcanaOutput:
    classification_prompt = build_classification_prompt(moment_description)
    classification_response = run_granite(classification_prompt)
    classification_result = _parse_and_validate(
        classification_response, ClassificationResult, "classification"
    )
    assert isinstance(classification_result, ClassificationResult)

    card_selection_prompt = build_card_selection_prompt(
        classification_result.model_dump_json()
    )
    card_selection_response = run_granite(card_selection_prompt)
    card_selection_result = _parse_and_validate(
        card_selection_response, CardSelectionResult, "card_selection"
    )
    assert isinstance(card_selection_result, CardSelectionResult)

    card_name = card_selection_result.card_name
    if card_name not in ARCANA_CARDS:
        raise ArcanaPipelineError(
            stage="card_selection",
            raw_output=card_selection_response,
            error_message=f"Selected card is not in the Arcana deck: {card_name}",
        )

    resolved_card = ResolvedCardSelection(
        card_name=card_name,
        card_id=CARD_IDS[card_name],
        reason=card_selection_result.reason,
    )

    card_metadata = ARCANA_CARDS[card_name]

    explanation_prompt = build_explanation_prompt(
        moment_description, card_name, card_metadata
    )
    explanation_response = run_granite(explanation_prompt)
    explanation_result = _parse_and_validate(
        explanation_response, ExplanationResult, "explanation"
    )
    assert isinstance(explanation_result, ExplanationResult)

    return ArcanaOutput(
        classification=classification_result,
        card=resolved_card,
        explanation=explanation_result,
    )


def interpret_match_moment(moment_description: str) -> str:
    prompt = f"""You are Soccer Arcana, an explainable AI that interprets soccer match moments using a deck of symbolic cards.

Match moment:
{moment_description}

Provide an Arcana reading with:
1. Card — Select the most fitting card from the Soccer Arcana deck (The Trickster, The Tower, The Surge, The Chaos Card, The Fortress, The Catalyst, The Shadow, The Sun, The Engine, The Mirror, The Wave, The Anchor) and name it.
2. Metaphor — A short metaphorical interpretation of what this moment means in the story of the match.
3. Tactics — A clear, simple explanation of the tactical meaning behind the moment.

Keep the response accessible and engaging for soccer fans."""

    return run_granite(prompt)
