from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from granite_client import generate_with_granite

router = APIRouter()


class GraniteRequest(BaseModel):
    prompt: str


@router.post("/granite")
def granite(request: GraniteRequest) -> dict[str, str]:
    output = generate_with_granite(request.prompt)
    return {"prompt": request.prompt, "output": output}


@router.get("/test/granite")
def test_granite_route() -> dict[str, Any]:
    try:
        output = generate_with_granite("Say hello in one sentence.")
        return {"output": output}
    except Exception:
        return {
            "error": True,
            "message": "Failed to call Granite.",
        }
