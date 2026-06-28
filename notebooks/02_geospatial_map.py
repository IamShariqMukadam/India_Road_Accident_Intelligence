# ============================================================
# NOTEBOOK 02 — GEOSPATIAL CHOROPLETH MAP
# India Road Accident Risk Map using Folium + GeoPandas
# ============================================================

# %% CELL 1 — Imports
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from folium import Choropleth, GeoJson
import json
import requests
import warnings
warnings.filterwarnings('ignore')

CLEAN = '../data/cleaned'
OUTPUT = '../outputs'

import os
os.makedirs(OUTPUT, exist_ok=True)

print("All imports OK")

# %% CELL 2 — Load your state_master (already cleaned from Day 1)
state_master = pd.read_csv(f'{CLEAN}/state_master.csv')
latest = state_master[state_master['year'] == 2024].copy()
latest = latest.dropna(subset=['accidents', 'fatalities'])
print(f"States in 2024 data: {latest['state'].nunique()}")
print(latest[['state','accidents','fatalities','fatality_rate_per_accident']].head())

# %% CELL 3 — Download India GeoJSON (verified working source)
GEOJSON_URL = 'https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/INDIA/INDIA_STATES.geojson'
r = requests.get(GEOJSON_URL, timeout=30)
india_geo = r.json()

# Save locally so you don't re-download every run
with open(f'{OUTPUT}/india_states.geojson', 'w') as f:
    json.dump(india_geo, f)

print(f"GeoJSON loaded: {len(india_geo['features'])} states/UTs")

# %% CELL 4 — Map GeoJSON state names to YOUR state_master names
# GeoJSON uses 'STNAME_SH' column — check exact names first:
geo_names = sorted([f['properties']['STNAME_SH'] for f in india_geo['features']])
print("GeoJSON names:", geo_names)

# %% CELL 5 — Name mapping: GeoJSON → your state_master names
# Some GeoJSON names differ from your cleaned data — this mapping fixes all mismatches
GEO_TO_MASTER = {
    'Andaman & Nicobar':       'Andaman & Nicobar Islands',
    'Andhra Pradesh':          'Andhra Pradesh',
    'Arunachal Pradesh':       'Arunachal Pradesh',
    'Assam':                   'Assam',
    'Bihar':                   'Bihar',
    'Chandigarh':              'Chandigarh',
    'Chhattisgarh':            'Chhattisgarh',
    'Dadra & Nagar Haveli':    'D&N Haveli and Daman & Diu',
    'Daman & Diu':             'D&N Haveli and Daman & Diu',  # merged UT
    'Delhi':                   'Delhi',
    'Goa':                     'Goa',
    'Gujarat':                 'Gujarat',
    'Haryana':                 'Haryana',
    'Himachal Pradesh':        'Himachal Pradesh',
    'Jammu & Kashmir':         'Jammu and Kashmir',
    'Jharkhand':               'Jharkhand',
    'Karnataka':               'Karnataka',
    'Kerala':                  'Kerala',
    'Ladakh':                  'Ladakh',
    'Lakshadweep':             'Lakshadweep',
    'Madhya Pradesh':          'Madhya Pradesh',
    'Maharashtra':             'Maharashtra',
    'Manipur':                 'Manipur',
    'Meghalaya':               'Meghalaya',
    'Mizoram':                 'Mizoram',
    'Nagaland':                'Nagaland',
    'Odisha':                  'Odisha',
    'Puducherry':              'Puducherry',
    'Punjab':                  'Punjab',
    'Rajasthan':               'Rajasthan',
    'Sikkim':                  'Sikkim',
    'Tamil Nadu':              'Tamil Nadu',
    'Telangana':               'Telangana',
    'Tripura':                 'Tripura',
    'Uttar Pradesh':           'Uttar Pradesh',
    'Uttarakhand':             'Uttarakhand',
    'West Bengal':             'West Bengal',
}

# Apply mapping to GeoJSON features
for feature in india_geo['features']:
    geo_name = feature['properties']['STNAME_SH']
    feature['properties']['state'] = GEO_TO_MASTER.get(geo_name, geo_name)

print("Name mapping applied.")

# %% CELL 6 — Merge GeoJSON with your data for tooltip info
# Build a lookup dict for fast access in tooltip
data_lookup = latest.set_index('state')[
    ['accidents','fatalities','fatality_rate_per_accident']
].to_dict('index')

print("Data lookup ready. Sample:")
print(list(data_lookup.items())[:2])

# %% CELL 7 — Build Map 1: Fatality Rate Choropleth (PRIMARY MAP)
# Center of India: 20.5937, 78.9629
m1 = folium.Map(
    location=[20.5937, 78.9629],
    zoom_start=5,
    tiles='CartoDB positron',   # clean light background
    prefer_canvas=True
)

# Build a dataframe for choropleth (needs state column + value column)
choropleth_data = latest[['state', 'fatality_rate_per_accident', 'accidents', 'fatalities']].copy()
choropleth_data['fatality_rate_per_accident'] = choropleth_data['fatality_rate_per_accident'].round(4)

# Save merged geojson for choropleth key
with open(f'{OUTPUT}/india_mapped.geojson', 'w') as f:
    json.dump(india_geo, f)

# Add choropleth layer — colored by fatality rate per accident
Choropleth(
    geo_data=f'{OUTPUT}/india_mapped.geojson',
    data=choropleth_data,
    columns=['state', 'fatality_rate_per_accident'],
    key_on='feature.properties.state',
    fill_color='RdYlGn_r',     # Red=dangerous, Green=safer
    fill_opacity=0.8,
    line_opacity=0.3,
    legend_name='Fatality Rate per Accident (2024) — Higher = More Dangerous',
    nan_fill_color='lightgray',
    nan_fill_opacity=0.4,
    highlight=True,
).add_to(m1)

# %% CELL 8 — Add hover tooltips (shows state name + all 3 metrics on hover)
tooltip_style = """
    background-color: #1a1a2e;
    color: white;
    font-family: Arial, sans-serif;
    font-size: 13px;
    padding: 8px 12px;
    border-radius: 6px;
    border: 1px solid #444;
"""

def style_function(feature):
    return {
        'fillOpacity': 0,
        'weight': 0,
    }

def highlight_function(feature):
    return {
        'fillOpacity': 0.2,
        'weight': 2,
        'color': '#333',
    }

GeoJson(
    india_geo,
    style_function=style_function,
    highlight_function=highlight_function,
    tooltip=folium.GeoJsonTooltip(
        fields=['state'],
        aliases=['State:'],
        localize=True,
        sticky=False,
        labels=True,
        style=tooltip_style,
        max_width=300,
    ),
    popup=folium.GeoJsonPopup(
        fields=['state'],
        aliases=['State'],
        localize=True,
    )
).add_to(m1)

# %% CELL 9 — Add custom markers with full stats popup for top 10 risk states
# Top 10 by fatality rate
top10 = latest.nlargest(10, 'fatality_rate_per_accident')

# Approximate state centroids (lat, lon) for marker placement
STATE_CENTROIDS = {
    'Bihar':            (25.0961, 85.3131),
    'Jharkhand':        (23.6102, 85.2799),
    'Punjab':           (31.1471, 75.3412),
    'Uttarakhand':      (30.0668, 79.0193),
    'Uttar Pradesh':    (26.8467, 80.9462),
    'Odisha':           (20.9517, 85.0985),
    'Gujarat':          (22.2587, 71.1924),
    'West Bengal':      (22.9868, 87.8550),
    'Haryana':          (29.0588, 76.0856),
    'Rajasthan':        (27.0238, 74.2179),
    'Tamil Nadu':       (11.1271, 78.6569),
    'Karnataka':        (15.3173, 75.7139),
    'Maharashtra':      (19.7515, 75.7139),
    'Madhya Pradesh':   (22.9734, 78.6569),
    'Kerala':           (10.8505, 76.2711),
    'Andhra Pradesh':   (15.9129, 79.7400),
    'Telangana':        (18.1124, 79.0193),
}

for _, row in top10.iterrows():
    state = row['state']
    if state not in STATE_CENTROIDS:
        continue
    lat, lon = STATE_CENTROIDS[state]
    rate = row['fatality_rate_per_accident']
    accidents = int(row['accidents'])
    fatalities = int(row['fatalities'])

    # Color based on severity
    if rate >= 0.7:
        color = 'red'
    elif rate >= 0.5:
        color = 'orange'
    else:
        color = 'yellow'

    folium.CircleMarker(
        location=[lat, lon],
        radius=10,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        popup=folium.Popup(
            f"""
            <div style='font-family:Arial; width:200px'>
            <b style='font-size:14px'>{state}</b><br>
            <hr style='margin:4px 0'>
            <b>Fatality Rate:</b> {rate:.4f}<br>
            <b>Accidents 2024:</b> {accidents:,}<br>
            <b>Fatalities 2024:</b> {fatalities:,}<br>
            <b>Risk Rank:</b> #{list(top10['state']).index(state)+1} in India
            </div>
            """,
            max_width=220
        ),
        tooltip=f"{state}: {rate:.4f} fatality rate"
    ).add_to(m1)

# Title
title_html = '''
<div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
     z-index:1000; background-color:white; padding: 10px 20px;
     border-radius:8px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
     font-family: Arial; text-align:center;">
    <b style="font-size:16px">India Road Accident Risk Map — 2024</b><br>
    <span style="font-size:12px; color:#666">Fatality Rate per Accident | Red markers = Top 10 highest-risk states</span>
</div>
'''
m1.get_root().html.add_child(folium.Element(title_html))

m1.save(f'{OUTPUT}/india_risk_map.html')
print("MAP 1 SAVED: outputs/india_risk_map.html")
print("Open this file in your browser — it's fully interactive.")

# %% CELL 10 — Build Map 2: Total Accidents Choropleth (SECOND MAP)
m2 = folium.Map(
    location=[20.5937, 78.9629],
    zoom_start=5,
    tiles='CartoDB positron'
)

Choropleth(
    geo_data=f'{OUTPUT}/india_mapped.geojson',
    data=choropleth_data,
    columns=['state', 'accidents'],
    key_on='feature.properties.state',
    fill_color='YlOrRd',
    fill_opacity=0.8,
    line_opacity=0.3,
    legend_name='Total Accidents 2024 (Raw Count)',
    nan_fill_color='lightgray',
    highlight=True,
).add_to(m2)

title_html2 = '''
<div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
     z-index:1000; background-color:white; padding: 10px 20px;
     border-radius:8px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
     font-family: Arial; text-align:center;">
    <b style="font-size:16px">India Road Accidents — Raw Count 2024</b><br>
    <span style="font-size:12px; color:#666">Compare with Risk Map to see why normalization matters</span>
</div>
'''
m2.get_root().html.add_child(folium.Element(title_html2))
m2.save(f'{OUTPUT}/india_accidents_map.html')
print("MAP 2 SAVED: outputs/india_accidents_map.html")
print("\nBOTH MAPS DONE. Open in browser with: firefox outputs/india_risk_map.html")
