# Small tests for my_part.py. Run with:  python test_my_part.py
import unittest

from my_part import bearing_degrees, distance_cells, nearby_aircraft


class TestMyPart(unittest.TestCase):
    def test_distance_3_4_5(self):
        self.assertEqual(distance_cells((0, 0), (3, 4)), 5.0)

    def test_distance_same_point(self):
        self.assertEqual(distance_cells((2, 2), (2, 2)), 0.0)

    def test_bearings(self):
        self.assertAlmostEqual(bearing_degrees((0, 0), (0, -1)), 0)    # north (y up the screen)
        self.assertAlmostEqual(bearing_degrees((0, 0), (1, 0)), 90)    # east
        self.assertAlmostEqual(bearing_degrees((0, 0), (0, 1)), 180)   # south
        self.assertAlmostEqual(bearing_degrees((0, 0), (-1, 0)), 270)  # west

    def test_nearby_sorted_and_notes(self):
        em = {"id": "SG-101", "x": 0, "y": 0}
        others = [
            {"id": "FAR", "x": 30, "y": 0},    # 240 km
            {"id": "NEAR", "x": 5, "y": 0},    # 40 km
            {"id": "MID", "x": 15, "y": 0},    # 120 km
        ]
        out = nearby_aircraft(em, others)
        self.assertEqual([p["id"] for p in out], ["NEAR", "MID", "FAR"])
        self.assertEqual(out[0]["d"], 40.0)
        self.assertEqual(out[0]["note"], "CLOSE - quick help")
        self.assertEqual(out[1]["note"], "")
        self.assertEqual(out[2]["note"], "TOO FAR")
        self.assertEqual(out[0]["b"], 90)

    def test_empty_list(self):
        self.assertEqual(nearby_aircraft({"id": "X", "x": 0, "y": 0}, []), [])


if __name__ == "__main__":
    unittest.main()
