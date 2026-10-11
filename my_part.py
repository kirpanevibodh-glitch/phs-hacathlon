# my_part.py - makes the "nearby planes" list for SOS ATC. 1 square on the map = 8 km
import math


def distance_cells(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


def bearing_degrees(a, b):  # 0 = north, 90 = east. y goes down on the map so north is -y
    return math.degrees(math.atan2(b[0] - a[0], a[1] - b[1])) % 360


def nearby_aircraft(emergency, others):
    out = []
    for p in others:
        e, q = (emergency["x"], emergency["y"]), (p["x"], p["y"])
        km = round(distance_cells(e, q) * 8, 1)
        out.append({"id": p["id"], "d": km, "b": round(bearing_degrees(e, q)), "note": "CLOSE - quick help" if km < 60 else "TOO FAR" if km > 200 else ""})
    return sorted(out, key=lambda r: r["d"])
