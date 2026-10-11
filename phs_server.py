# phs_server.py - shows phs.html and gets real planes. run: python phs_server.py, then go to http://localhost:8000
# for flightradar24 set a token first: $env:FR24_API_TOKEN = "your-token" (without one it uses adsb.lol, free)
import json, os, time, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import my_part  # makes the nearby planes list

HERE = os.path.dirname(os.path.abspath(__file__))

TOKEN = os.environ.get("FR24_API_TOKEN", "")
N, W = 47.2, 6.0  # map corners, same as latLon() in phs.html
S, E = N - 40 * 8 / 111, W + 60 * 8 / 75.7
cache = {"at": 0, "answer": None}


def get(url, headers={}):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "sos-atc", **headers}), timeout=10))


def live_planes():
    if time.time() - cache["at"] < (10 if TOKEN else 5):  # don't ask too often (flightradar24 costs money per request)
        return cache["answer"]
    source = "Flightradar24" if TOKEN else "adsb.lol"
    try:
        if TOKEN:
            raw = get(f"https://fr24api.flightradar24.com/api/live/flight-positions/light?bounds={N},{S},{W},{E}", {"Authorization": "Bearer " + TOKEN, "Accept-Version": "v1"})["data"]
            planes = [{"callsign": a.get("callsign") or a.get("hex"), "type": a.get("type", ""), "lat": a["lat"], "lon": a["lon"], "alt_ft": a.get("alt"),
                       "gs_kt": a.get("gspeed"), "track": a.get("track", 0), "squawk": str(a.get("squawk") or "")} for a in raw]
        else:
            raw = get(f"https://api.adsb.lol/v2/point/{(N + S) / 2:.3f}/{(W + E) / 2:.3f}/170")["ac"]
            planes = [{"callsign": (a.get("flight") or a.get("hex")).strip(), "type": a.get("t", ""), "lat": a.get("lat"), "lon": a.get("lon"),
                       "alt_ft": 0 if a.get("alt_baro") == "ground" else a.get("alt_baro"), "gs_kt": a.get("gs"), "track": a.get("track", 0), "squawk": str(a.get("squawk") or "")} for a in raw]
        planes = [p for p in planes if p["lat"] is not None and S <= p["lat"] <= N and W <= p["lon"] <= E]
        for p in planes:
            p["emergency"] = p["squawk"] in ("7500", "7600", "7700")
        cache["answer"] = {"ok": True, "source": source, "aircraft": planes}
    except Exception as err:
        cache["answer"] = {"ok": False, "error": f"couldn't get planes from {source}: {err}"}
    cache["at"] = time.time()
    return cache["answer"]


class Server(BaseHTTPRequestHandler):
    def reply(self, body, kind="application/json", code=200):
        self.send_response(code)
        self.send_header("Content-Type", kind)
        self.send_header("Access-Control-Allow-Origin", "*")  # so it also works from vs code live server
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body if isinstance(body, bytes) else json.dumps(body).encode())

    def do_GET(self):
        if self.path.startswith("/api/ping"): self.reply({"ok": True})
        elif self.path.startswith("/api/live"): self.reply(live_planes())
        else: self.reply(open(os.path.join(HERE, "phs.html"), "rb").read(), "text/html; charset=utf-8")

    def do_OPTIONS(self):  # the browser asks this before a POST from another page
        self.reply(b"", code=204)

    def do_POST(self):  # /api/nearby
        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.reply({"ok": True, "nearby": my_part.nearby_aircraft(data["emergency"], data["others"])})

    def log_message(self, *args):
        pass


print("SOS ATC is running at http://localhost:8000 - live planes from", "Flightradar24" if TOKEN else "adsb.lol")
ThreadingHTTPServer(("localhost", 8000), Server).serve_forever()
