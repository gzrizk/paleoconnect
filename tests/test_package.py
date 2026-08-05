from __future__ import annotations

import pathlib

from paleoconnect import ConnectivityResult, LandmassDefinitions


class TestLandmassDefinitions:
    def test_from_dict(self) -> None:
        ld = LandmassDefinitions.from_dict({"A": [1, 2], "B": [3]})
        assert ld.names == ["A", "B"]
        assert ld.pairs == [("A", "B")]
        assert ld.plate_ids("A") == [1, 2]
        assert len(ld) == 2
        assert "A" in ld
        assert "C" not in ld

    def test_single_landmass_no_pairs(self) -> None:
        ld = LandmassDefinitions.from_dict({"A": [1]})
        assert ld.pairs == []

    def test_multiple_pairs(self) -> None:
        ld = LandmassDefinitions.from_dict({"A": [1], "B": [2], "C": [3]})
        assert set(ld.pairs) == {("A", "B"), ("A", "C"), ("B", "C")}

    def test_from_toml(self, tmp_path: object) -> None:
        path = pathlib.Path(str(tmp_path)) / "landmasses.toml"
        path.write_text("[landmasses]\nA = [1, 2]\nB = [3]\n")
        ld = LandmassDefinitions.from_toml(path)
        assert ld.names == ["A", "B"]


class TestConnectivityResult:
    def test_add_and_to_dataframe(self) -> None:
        result = ConnectivityResult()
        result.add(time=280.0, landmass_a="X", landmass_b="Y", distance_km=1500.0)
        result.add(time=279.0, landmass_a="X", landmass_b="Y", distance_km=1490.0)
        df = result.to_dataframe()
        assert len(df) == 2
        assert list(df.columns) == ["time_ma", "landmass_a", "landmass_b", "distance_km"]
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
