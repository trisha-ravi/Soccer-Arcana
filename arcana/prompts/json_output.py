import json
from typing import Any

from pydantic import BaseModel


def build_json_output_section(
    model: type[BaseModel],
    example: dict[str, Any],
) -> str:
    """Build standardized JSON output instructions for Granite prompts."""
    field_names = ", ".join(f'"{name}"' for name in model.model_fields)
    example_json = json.dumps(example, indent=2)
    schema_json = json.dumps(model.model_json_schema(), indent=2)

    return f"""Required JSON fields (use these exact field names):
{field_names}

Example JSON object:
{example_json}

JSON output rules:
- Do not include any extra text, commentary, or markdown before or after the JSON.
- Never include trailing commas in the JSON.
- Never wrap the JSON in backticks or code fences.
- The response must parse directly into the required schema.

Return your answer ONLY as valid JSON matching this schema:
{schema_json}"""
