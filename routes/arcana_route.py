from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from arcana.pipeline import ArcanaPipelineError, run_arcana_pipeline
from arcana.schema import ArcanaOutput

router = APIRouter()

TEST_MOMENT = "A winger nutmegs a defender and breaks into space."

_STAGE_LABELS = {
    "classification": "classification",
    "card_selection": "card selection",
    "explanation": "explanation",
}


class ArcanaRequest(BaseModel):
    moment_description: str


def _pipeline_error_response(exc: ArcanaPipelineError) -> dict[str, Any]:
    return {
        "error": True,
        "stage": _STAGE_LABELS.get(exc.stage, exc.stage),
        "message": exc.error_message,
        "raw_output": exc.raw_output,
    }


def _unexpected_error_response() -> dict[str, Any]:
    return {
        "error": True,
        "stage": "unknown",
        "message": "An unexpected error occurred while processing the Arcana reading.",
    }


@router.post("/arcana")
def arcana(request: ArcanaRequest) -> ArcanaOutput | dict[str, Any]:
    try:
        result = run_arcana_pipeline(request.moment_description)
        return result
    except ArcanaPipelineError as exc:
        return _pipeline_error_response(exc)
    except Exception:
        return _unexpected_error_response()


@router.get("/test/arcana")
def test_arcana() -> ArcanaOutput | dict[str, Any]:
    try:
        return run_arcana_pipeline(TEST_MOMENT)
    except ArcanaPipelineError as exc:
        return _pipeline_error_response(exc)
    except Exception:
        return _unexpected_error_response()
