from pathlib import Path

import pandas as pd
import pybamm
import pytest
import yaml

from battery_lab.pybamm_baseline import build_model, run


@pytest.mark.parametrize(
    ("parameter_set", "thermal"),
    [
        ("Prada2013", "isothermal"),
        ("ORegan2022", "lumped"),
    ],
)
def test_reference_parameter_sets_process(parameter_set: str, thermal: str) -> None:
    model = build_model({"model": "DFN", "thermal": thermal})
    parameters = pybamm.ParameterValues(parameter_set)
    parameters.process_model(model)


def test_short_electrothermal_run(tmp_path: Path) -> None:
    config = {
        "project_id": "battery-ai-comsol-lab",
        "chemistry": "graphite_NMC_LG_M50",
        "cell_format": "cylindrical",
        "engine": "pybamm",
        "model": "DFN",
        "thermal": "lumped",
        "parameter_set": "ORegan2022",
        "protocol_id": "ci_smoke_discharge",
        "c_rate": 0.5,
        "ambient_temperature_K": 298.15,
        "initial_soc": 0.8,
        "max_duration_s": 30,
        "output_points": 5,
    }
    config_path = tmp_path / "smoke.yaml"
    config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")

    csv_path, manifest_path = run(config_path, tmp_path / "run")

    frame = pd.read_csv(csv_path)
    assert not frame.empty
    assert {"time_s", "current_A", "voltage_V", "temperature_K"} <= set(frame.columns)
    assert frame["temperature_K"].notna().all()
    assert manifest_path.exists()
