from __future__ import annotations

import pathlib

import pytest

from paleoconnect import ConnectivityResult


class TestConnectivityResult:
    def test_add_and_to_dataframe(self) -> None:
        result = ConnectivityResult()
        result.add(time=280.0, landmass_a="X", landmass_b="Y", distance_km=1500.0)
        result.add(time=279.0, landmass_a="X", landmass_b="Y", distance_km=1490.0)
        df = result.to_dataframe()
        assert len(df) == 2
        assert list(df.columns) == [
            "time_ma",
            "landmass_a",
            "landmass_b",
            "distance_km",
        ]
        assert df["distance_km"].iloc[0] == 1500.0

    def test_empty_result(self) -> None:
        result = ConnectivityResult()
        assert len(result) == 0
        assert not result
        assert result.to_dataframe().empty

    def test_summary(self) -> None:
        result = ConnectivityResult()
        result.add(280, "A", "B", 1000.0)
        result.add(279, "A", "B", 2000.0)
        result.add(280, "A", "C", 500.0)
        s = result.summary()
        assert len(s) == 2
        row_ab = s[s["landmass_a"] == "A"].iloc[0]
        assert row_ab["min_km"] == 1000.0
        assert row_ab["max_km"] == 2000.0
        assert row_ab["mean_km"] == 1500.0

    def test_to_csv(self, tmp_path: object) -> None:
        result = ConnectivityResult()
        result.add(280, "A", "B", 1500.0)
        path = pathlib.Path(str(tmp_path)) / "out.csv"
        result.to_csv(path)
        content = path.read_text()
        assert "time_ma" in content
        assert "1500.0" in content


pygplates = pytest.importorskip("pygplates", reason="pyGPlates not installed")


class TestConnectivityModel:
    def test_find_component_pangea_at_permian(self) -> None:
        from paleoconnect import ConnectivityModel

        rot = pathlib.Path(__file__).parent.parent / "data" / "plate_models" / "Merdith_etal_2021" / "Rotations" / "1000_0_rotfile_Merdith_etal.rot"

        topo = pathlib.Path(__file__).parent.parent / "data" / "plate_models" / "Merdith_etal_2021" / "Topologies" / "410-250_plate_bounds_Merdith_etal.gpml"

        if not rot.exists() or not topo.exists():
            pytest.skip("Merdith model data not available")

        model = ConnectivityModel(
            rotation_files=[rot],
            topology_files=[topo],
        )

        comp_africa = model._find_component(280.0, 701)
        comp_north_china = model._find_component(280.0, 601)
        comp_south_china = model._find_component(280.0, 602)

        assert 101 in comp_africa, "Laurentia should be in Pangea"
        assert 201 in comp_africa, "South America should be in Pangea"
        assert 802 in comp_africa, "Antarctica should be in Pangea"
        assert 801 in comp_africa, "Australia should be in Pangea"

        assert 601 not in comp_africa, "North China should NOT be in Pangea"
        assert 601 in comp_north_china, "North China should be its own component"

        assert 602 not in comp_africa, "South China should NOT be in Pangea"
        assert 602 in comp_south_china, "South China should be its own component"

        assert comp_north_china != comp_south_china
