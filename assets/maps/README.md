# Map data

`world.geojson` is Natural Earth 1:110m admin-0 countries, v5.1.2:
https://github.com/nvkelso/natural-earth-vector/blob/v5.1.2/geojson/ne_110m_admin_0_countries.geojson

Natural Earth data is public domain: https://www.naturalearthdata.com/about/terms-of-use/
`countries/*.geojson` contains Natural Earth 1:10m admin-0 country outlines from the same v5.1.2 repository snapshot:
https://github.com/nvkelso/natural-earth-vector/blob/v5.1.2/geojson/ne_10m_admin_0_countries.geojson

The country data is split by ISO_A2_EH (falling back to ISO_A2), keeps only code/name metadata,
and rounds coordinate decimals to five places. Features without a two-letter ISO code are omitted.
The same country files also include internal admin-1 lines (provinces, states, prefectures, or equivalent units):
https://github.com/nvkelso/natural-earth-vector/blob/v5.1.2/geojson/ne_10m_admin_1_states_provinces_lines.geojson

Boundary features are joined through ADM0_A3 to the country's ISO code, tagged `layer: admin1`,
and rendered as unfilled lines above the country outline (`layer: country`). Countries without
admin-1 features in this dataset retain their outline alone. These are geographic overview data,
not guaranteed to reflect the latest administrative reorganizations.

There are 239 files, about 19.97 MiB in total; browsers only download the selected country's file.
Successful loads are reused while the page remains open, and switching back to the world removes internal boundaries.

These scales mean 1:110,000,000 for the world and 1:10,000,000 for country detail, not meter resolutions.
They provide geographic outlines and first-order internal boundaries, not streets or city/county boundaries. Boundaries reflect the source dataset.
Coordinates use WGS84. Country filters fit the detailed feature bounds; "all" fits the lightweight world map.
The selected country's coarse feature is replaced by its detailed geometry; neighboring countries keep the overview geometry.
If detail loading fails, the overview remains available. Selecting the country again retries the download.
No API key, geocoding, third-party tiles or runtime external requests are needed.

Leaflet 1.9.4 is vendored in `../vendor/leaflet/`, with its BSD-2-Clause license.

To regenerate the detail files, download both linked source GeoJSON files and run:

```text
python scripts/prepare_gallery_maps.py path/to/ne_10m_admin_0_countries.geojson --subdivisions path/to/ne_10m_admin_1_states_provinces_lines.geojson
```

Normal website builds do not download or regenerate map data.
