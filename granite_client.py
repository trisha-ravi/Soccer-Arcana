"""Client for IBM Granite models via watsonx.ai."""

from __future__ import annotations

import os
from typing import Any

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model

# --- Model identity ---
# IBM withdrew granite-13b-instruct; use a current Granite instruct model.
DEFAULT_MODEL_ID = "ibm/granite-3-8b-instruct"
DEFAULT_URL = "https://us-south.ml.cloud.ibm.com"

# --- Generation parameters (adjust for deterministic vs creative behavior) ---
#
# Granite Agents workshops (deterministic, reliable tool-calling):
#   decoding_method = "greedy", temperature = 0, max_new_tokens = 250
#
# Creative Arcana readings (more varied, metaphorical output):
#   decoding_method = "sample", temperature = 0.7, max_new_tokens = 300

# "greedy" picks the highest-probability token each step (factual, repeatable).
# "sample" randomly chooses from likely tokens (creative, more variable).
DECODING_METHOD = "sample"

# 0.0 = greedy/deterministic; higher values (up to 2.0) increase creativity.
# Agents workshops set this to 0 to limit hallucinations.
TEMPERATURE = 0.2

# Minimum tokens generated before stop sequences can take effect.
# Agents workshops often use 5 to avoid very short incomplete answers.
MIN_NEW_TOKENS = 0

# Upper limit on generated output length. Increase if readings are cut off.
# Agents workshops typically use 250; Prompt Lab default is 200.
MAX_NEW_TOKENS = 300

# Top-k: sample from the k most likely tokens (1–100). Higher = more variety.
# watsonx default is 50. Greedy decoding is equivalent to top_k = 1.
TOP_K = 50

# Top-p (nucleus sampling): sample until cumulative probability reaches this
# threshold (0.0–1.0). Lower values filter out low-probability tokens.
# Default 1.0 means top-p is effectively unused unless you lower it.
TOP_P = 1.0

# Set to a fixed integer (e.g. 42) for repeatable sampling results across runs.
# Leave as None to let watsonx generate a random seed each time.
RANDOM_SEED: int | None = None

# 1.0 = no penalty; values above 1.0 discourage repeated phrases in output.
REPETITION_PENALTY = 1.0

# Strings that halt generation when they appear in the output.
# Agents workshops use ["Human:", "Observation"] to stop the model from
# inventing fake user turns or extra agent steps.
STOP_SEQUENCES: list[str] = []


def _build_granite_params() -> dict[str, Any]:
    params: dict[str, Any] = {
        "decoding_method": DECODING_METHOD,
        "temperature": TEMPERATURE,
        "min_new_tokens": MIN_NEW_TOKENS,
        "max_new_tokens": MAX_NEW_TOKENS,
        "top_k": TOP_K,
        "top_p": TOP_P,
        "repetition_penalty": REPETITION_PENALTY,
    }
    if RANDOM_SEED is not None:
        params["random_seed"] = RANDOM_SEED
    if STOP_SEQUENCES:
        params["stop_sequences"] = STOP_SEQUENCES
    return params


DEFAULT_PARAMS = _build_granite_params()


class GraniteClient:
    """Thin wrapper around watsonx.ai Model for Granite text generation."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        project_id: str | None = None,
        url: str | None = None,
        model_id: str | None = None,
        params: dict[str, Any] | None = None,
    ) -> None:
        api_key = api_key or os.environ["WATSONX_APIKEY"]
        project_id = project_id or os.environ["WATSONX_PROJECT_ID"]
        url = url or os.getenv("WATSONX_URL", DEFAULT_URL)
        model_id = model_id or os.getenv("WATSONX_MODEL_ID", DEFAULT_MODEL_ID)

        credentials = Credentials(url=url, api_key=api_key)

        self._model = Model(
            model_id=model_id,
            credentials=credentials,
            project_id=project_id,
            params=params or DEFAULT_PARAMS,
        )

    def generate(self, prompt: str) -> str:
        """Generate text from a prompt."""
        return self._model.generate_text(prompt=prompt)


_granite: GraniteClient | None = None


def _get_granite() -> GraniteClient:
    global _granite
    if _granite is None:
        _granite = GraniteClient()
    return _granite


def generate_with_granite(prompt: str) -> str:
    return _get_granite().generate(prompt=prompt)


def test_granite() -> str:
    result = generate_with_granite("Hello Granite")
    print(result)
    return result
