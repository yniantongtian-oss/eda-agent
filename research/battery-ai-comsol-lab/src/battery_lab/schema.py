from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field


class SimulationManifest(BaseModel):
    """Run-level provenance shared by physics and ML workflows."""

    simulation_id: str
    project_id: str = "battery-ai-comsol-lab"
    engine: Literal["pybamm", "comsol", "other"]
    engine_version: str | None = None
    model_id: str
    chemistry: str
    cell_format: str = "generic"
    parameter_set_id: str
    geometry_id: str | None = None
    protocol_id: str
    created_at_utc: datetime = Field(default_factory=lambda: datetime.now(UTC))
    commit_sha: str | None = None
    config_path: str | None = None
    status: Literal["created", "running", "completed", "failed"] = "created"
    warnings: list[str] = Field(default_factory=list)
    inputs: dict[str, Any] = Field(default_factory=dict)
    outputs: dict[str, str] = Field(default_factory=dict)

    def write_json(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.model_dump_json(indent=2), encoding="utf-8")


def load_yaml(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data
