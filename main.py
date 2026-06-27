from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from arcana.pipeline import interpret_match_moment
from granite_client import generate_with_granite
from routes.arcana_route import router as arcana_router
from routes.granite_route import router as granite_router

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Soccer Arcana")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(granite_router)
app.include_router(arcana_router)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


class MomentRequest(BaseModel):
    moment: str


@app.post("/interpret")
def interpret(request: MomentRequest) -> dict[str, str]:
    granite_output = interpret_match_moment(request.moment)
    return {"moment": request.moment, "interpretation": granite_output}


@app.get("/test-granite")
def test_granite_endpoint() -> dict[str, str]:
    return {"result": test_granite()}


def test_granite() -> str:
    result = generate_with_granite("Explain The Trickster card in simple terms.")
    print(result)
    return result


if __name__ == "__main__":
    moment = input("Describe a match moment: ")
    granite_output = interpret_match_moment(moment)
    print(granite_output)
