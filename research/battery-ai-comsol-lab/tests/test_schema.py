from pathlib import Path

import pytest

from battery_lab.schema import SimulationManifest, load_yaml


def test_manifest_round_trip(tmp_path: Path) -> None:
    manifest = SimulationManifest(
        simulation_id="sim_test_001",
        engine="pybamm",
        model_id="DFN_lumped",
        chemistry="LFP_graphite",
        parameter_set_id="Prada2013",
        protocol_id="constant_current_discharge",
    )
    path = tmp_path / "manifest.json"
    manifest.write_json(path)
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert '"simulation_id": "sim_test_001"' in text
    assert '"engine": "pybamm"' in text


def test_manifest_rejects_unknown_engine() -> None:
    with pytest.raises(ValueError):
        SimulationManifest(
            simulation_id="bad",
            engine="mystery",
            model_id="x",
            chemistry="x",
            parameter_set_id="x",
            protocol_id="x",
        )


def test_load_yaml_requires_mapping(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("- one\n- two\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_yaml(path)
