from pydantic import BaseModel, Field


class ClassificationResult(BaseModel):
    moment_type: str
    confidence: float = Field(ge=0.0, le=1.0)


class CardSelectionResult(BaseModel):
    card_name: str
    reason: str


class ResolvedCardSelection(BaseModel):
    card_name: str
    card_id: str
    reason: str


class ExplanationResult(BaseModel):
    metaphor: str
    tactical_explanation: str
    cultural_context: str
    emotional_impact: str


class ArcanaOutput(BaseModel):
    classification: ClassificationResult
    card: ResolvedCardSelection
    explanation: ExplanationResult


__all__ = [
    "ArcanaOutput",
    "CardSelectionResult",
    "ClassificationResult",
    "ExplanationResult",
    "ResolvedCardSelection",
]
