from __future__ import annotations

from pathlib import Path
from typing import Any


class ComsolUnavailableError(RuntimeError):
    """Raised when COMSOL/MPh is not available in the current environment."""


class ComsolSession:
    """Small deterministic adapter around MPh for battery research workflows.

    The adapter intentionally exposes only a narrow set of operations used by
    reproducible research scripts. A local COMSOL installation and valid
    license are required; this package does not redistribute COMSOL.
    """

    def __init__(self, cores: int | None = None) -> None:
        try:
            import mph
        except ImportError as exc:
            raise ComsolUnavailableError(
                "MPh is not installed. Install the optional dependency with "
                "`pip install -e .[comsol]` and ensure COMSOL is installed locally."
            ) from exc

        self._mph = mph
        start_kwargs: dict[str, Any] = {}
        if cores is not None:
            start_kwargs["cores"] = cores
        self.client = mph.start(**start_kwargs)
        self.model = None

    def open_model(self, path: str | Path) -> None:
        self.model = self.client.load(str(Path(path)))

    def _require_model(self):
        if self.model is None:
            raise RuntimeError("No COMSOL model is open")
        return self.model

    def set_parameters(self, values: dict[str, str | int | float]) -> None:
        model = self._require_model()
        for name, value in values.items():
            model.parameter(name, str(value))

    def run_study(self, study_name: str | None = None) -> None:
        model = self._require_model()
        model.solve(study_name)

    def evaluate(self, expressions: str | list[str], unit: str | None = None):
        model = self._require_model()
        return model.evaluate(expressions, unit=unit)

    def save_copy(self, path: str | Path) -> None:
        model = self._require_model()
        model.save(str(Path(path)))

    def close_model(self) -> None:
        if self.model is not None:
            try:
                self.client.remove(self.model)
            finally:
                self.model = None

    def __enter__(self) -> "ComsolSession":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close_model()
