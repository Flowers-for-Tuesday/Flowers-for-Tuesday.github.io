"""Split a local Natural Earth 1:10m GeoJSON into compact, lazy-loadable country files.

Usage: python scripts/prepare_gallery_maps.py countries.geojson --subdivisions admin1_lines.geojson
This maintenance command is separate from the offline website build.
"""
import argparse
import json
from pathlib import Path
import re


def round_coordinates(value):
    if isinstance(value, list):
        return [round_coordinates(part) for part in value]
    return round(value, 5)


def prepare(source, target, subdivisions):
    countries = {}
    country_codes = {}
    for feature in json.loads(source.read_text(encoding="utf-8"))["features"]:
        properties = feature["properties"]
        code = properties.get("ISO_A2_EH") or properties.get("ISO_A2")
        if not isinstance(code, str) or not re.fullmatch(r"[A-Z]{2}", code):
            continue
        country_codes[properties["ADM0_A3"]] = code
        countries.setdefault(code, []).append({
            "type": "Feature",
            "properties": {"country": code, "layer": "country", "name": properties.get("NAME_ZH") or properties.get("ADMIN", code)},
            "geometry": {"type": feature["geometry"]["type"], "coordinates": round_coordinates(feature["geometry"]["coordinates"])},
        })
    # Append internal boundaries after the country outline so they render above its fill.
    for feature in json.loads(subdivisions.read_text(encoding="utf-8"))["features"]:
        code = country_codes.get(feature["properties"].get("ADM0_A3"))
        geometry = feature.get("geometry")
        if code not in countries or not geometry or geometry["type"] not in {"LineString", "MultiLineString"}:
            continue
        countries[code].append({
            "type": "Feature",
            "properties": {"country": code, "layer": "admin1"},
            "geometry": {"type": geometry["type"], "coordinates": round_coordinates(geometry["coordinates"])},
        })
    target.mkdir(parents=True, exist_ok=True)
    size = 0
    for code, features in sorted(countries.items()):
        output = target / f"{code}.geojson"
        payload = json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False, separators=(",", ":")) + "\n"
        output.write_text(payload, encoding="utf-8")
        size += len(payload.encode("utf-8"))
    print(f"Prepared {len(countries)} country maps, {size / 1024 / 1024:.2f} MiB total.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--subdivisions", type=Path, required=True, help="Natural Earth admin-1 boundary lines GeoJSON")
    args = parser.parse_args()
    prepare(args.source, Path(__file__).resolve().parents[1] / "assets/maps/countries", args.subdivisions)
