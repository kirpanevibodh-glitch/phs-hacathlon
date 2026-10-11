# SOS ATC

Our hackathon project. A pretend air traffic control screen for a plane in an emergency.
Everything in it is made up — it's **not** real flight software.

What it does:
- plans a route around storms and mountains and writes it out step by step (heading, altitude, distance)
- you pick which airport the emergency plane lands at
- other planes can be asked to help, and they get their own steps to meet it somewhere safe
- a pilot view in a second tab that stays in sync
- live planes from adsb.lol (or Flightradar24 if you have a token) and live weather from Open-Meteo

## Run it

Needs Python 3, nothing to install.

```
python phs_server.py
```

Then open http://localhost:8000

For Flightradar24 instead of adsb.lol, set a token first:

```
$env:FR24_API_TOKEN = "your-token"
```

## Files

- `phs.html` - the whole page (map, steps, helpers, pilot view)
- `phs_server.py` - small server for the page and the live planes
- `my_part.py` - makes the "nearby planes" list
- `test_my_part.py` - tests, run `python test_my_part.py`
