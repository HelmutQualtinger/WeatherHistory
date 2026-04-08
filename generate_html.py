#!/usr/bin/env python3
"""
generate_html.py – reads weather CSVs and produces a self-contained dashboard.html.
Usage: python3 generate_html.py
"""

import sys
import json
import math
from pathlib import Path

import numpy as np
import plotly.express as px

# Make the project root importable so weather_dash_lib can be found from any cwd.
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from weather_dash_lib import load_data, MONATSNAMEN  # noqa: E402

# ---------------------------------------------------------------------------
# City / continent / coordinate config  (mirrors StrahlungDashAlle.py)
# ---------------------------------------------------------------------------
STAEDTE = {
    "Wien":        {"filename":"csv/wien_wetter_vollständig_03_2026.csv","h1_color_light":"#2c3e50","h1_color_dark":"#aed6f1","strahlung_colorscale":"YlOrRd","bar_voll_color":"#e67e22","bar_aktuell_color":"#f39c12","precip_color":"#2980b9","temp_cold_threshold":0,"temp_hot_threshold":20,"temp_colors":["#3498db","#f39c12","#e74c3c"]},
    "Lagos":       {"filename":"csv/lagos_wetter_vollständig_03_2026.csv","h1_color_light":"#117a65","h1_color_dark":"#76d7c4","strahlung_colorscale":"YlOrRd","bar_voll_color":"#d35400","bar_aktuell_color":"#f0b27a","precip_color":"#1a5276","temp_cold_threshold":22,"temp_hot_threshold":32,"temp_colors":["#f39c12","#e74c3c","#7b241c"]},
    "Nairobi":     {"filename":"csv/nairobi_wetter_vollständig_03_2026.csv","h1_color_light":"#1e6b3c","h1_color_dark":"#82e0aa","strahlung_colorscale":"YlGn","bar_voll_color":"#27ae60","bar_aktuell_color":"#82e0aa","precip_color":"#1e6b3c","temp_cold_threshold":15,"temp_hot_threshold":28,"temp_colors":["#3498db","#f39c12","#e74c3c"]},
    "Casablanca":  {"filename":"csv/casablanca_wetter_vollständig_03_2026.csv","h1_color_light":"#1a5276","h1_color_dark":"#7fb3d3","strahlung_colorscale":"solar","bar_voll_color":"#2980b9","bar_aktuell_color":"#85c1e9","precip_color":"#1a5276","temp_cold_threshold":15,"temp_hot_threshold":28,"temp_colors":["#3498db","#f39c12","#e74c3c"]},
    "Medina":      {"filename":"csv/medina_wetter_vollständig_03_2026.csv","h1_color_light":"#6e2f00","h1_color_dark":"#e59866","strahlung_colorscale":"Oranges","bar_voll_color":"#c0392b","bar_aktuell_color":"#e59866","precip_color":"#c0392b","temp_cold_threshold":25,"temp_hot_threshold":35,"temp_colors":["#f39c12","#c0392b","#7b241c"]},
    "Rom":         {"filename":"csv/rome_wetter_vollständig_03_2026.csv","h1_color_light":"#7b241c","h1_color_dark":"#f1948a","strahlung_colorscale":"Reds","bar_voll_color":"#c0392b","bar_aktuell_color":"#e59866","precip_color":"#7b241c","temp_cold_threshold":5,"temp_hot_threshold":25,"temp_colors":["#3498db","#f39c12","#e74c3c"]},
    "Lissabon":    {"filename":"csv/lisbon_wetter_vollständig_03_2026.csv","h1_color_light":"#1a6b8a","h1_color_dark":"#76d7c4","strahlung_colorscale":"Blues","bar_voll_color":"#2471a3","bar_aktuell_color":"#7fb3d3","precip_color":"#1a6b8a","temp_cold_threshold":10,"temp_hot_threshold":25,"temp_colors":["#3498db","#f39c12","#e74c3c"]},
    "Santiago":    {"filename":"csv/santiago_wetter_vollständig_03_2026.csv","h1_color_light":"#6c3483","h1_color_dark":"#d2b4de","strahlung_colorscale":"Purples","bar_voll_color":"#7d3c98","bar_aktuell_color":"#d2b4de","precip_color":"#6c3483","temp_cold_threshold":10,"temp_hot_threshold":25,"temp_colors":["#3498db","#f39c12","#e74c3c"]},
    "Las Vegas":   {"filename":"csv/lasvegas_wetter_vollständig_03_2026.csv","h1_color_light":"#7d6608","h1_color_dark":"#f7dc6f","strahlung_colorscale":"YlOrRd","bar_voll_color":"#d4ac0d","bar_aktuell_color":"#f9e79f","precip_color":"#7d6608","temp_cold_threshold":10,"temp_hot_threshold":35,"temp_colors":["#3498db","#f39c12","#e74c3c"]},
    "Los Angeles": {"filename":"csv/losangeles_wetter_vollständig_03_2026.csv","h1_color_light":"#b7950b","h1_color_dark":"#f9e79f","strahlung_colorscale":"YlOrBr","bar_voll_color":"#d4ac0d","bar_aktuell_color":"#f9e79f","precip_color":"#b7950b","temp_cold_threshold":12,"temp_hot_threshold":28,"temp_colors":["#3498db","#f39c12","#e74c3c"]},
    "New York":    {"filename":"csv/newyork_wetter_vollständig_03_2026.csv","h1_color_light":"#1a3a5c","h1_color_dark":"#85c1e9","strahlung_colorscale":"Blues","bar_voll_color":"#2471a3","bar_aktuell_color":"#85c1e9","precip_color":"#1a3a5c","temp_cold_threshold":0,"temp_hot_threshold":25,"temp_colors":["#3498db","#f39c12","#e74c3c"]},
    "Oslo":        {"filename":"csv/oslo_wetter_vollständig_03_2026.csv","h1_color_light":"#117a65","h1_color_dark":"#76d7c4","strahlung_colorscale":"BuGn","bar_voll_color":"#148f77","bar_aktuell_color":"#76d7c4","precip_color":"#117a65","temp_cold_threshold":0,"temp_hot_threshold":18,"temp_colors":["#3498db","#f39c12","#e74c3c"]},
    "Yakutsk":     {"filename":"csv/yakutsk_wetter_vollständig_03_2026.csv","h1_color_light":"#1a3a5c","h1_color_dark":"#aed6f1","strahlung_colorscale":"Blues","bar_voll_color":"#2471a3","bar_aktuell_color":"#aed6f1","precip_color":"#1a3a5c","temp_cold_threshold":-30,"temp_hot_threshold":15,"temp_colors":["#3498db","#f39c12","#e74c3c"]},
    "Tokyo":       {"filename":"csv/tokyo_wetter_vollständig_03_2026.csv","h1_color_light":"#1b4f8a","h1_color_dark":"#85c1e9","strahlung_colorscale":"Blues","bar_voll_color":"#2471a3","bar_aktuell_color":"#85c1e9","precip_color":"#1b4f8a","temp_cold_threshold":5,"temp_hot_threshold":25,"temp_colors":["#3498db","#f39c12","#e74c3c"]},
    "Shanghai":    {"filename":"csv/shanghai_wetter_vollständig_03_2026.csv","h1_color_light":"#922b21","h1_color_dark":"#f1948a","strahlung_colorscale":"Reds","bar_voll_color":"#c0392b","bar_aktuell_color":"#f1948a","precip_color":"#922b21","temp_cold_threshold":5,"temp_hot_threshold":28,"temp_colors":["#3498db","#f39c12","#e74c3c"]},
    "Mumbai":      {"filename":"csv/mumbai_wetter_vollständig_03_2026.csv","h1_color_light":"#784212","h1_color_dark":"#f0b27a","strahlung_colorscale":"Oranges","bar_voll_color":"#ca6f1e","bar_aktuell_color":"#f0b27a","precip_color":"#1a5276","temp_cold_threshold":20,"temp_hot_threshold":32,"temp_colors":["#f39c12","#e74c3c","#7b241c"]},
    "Dublin":      {"filename":"csv/dublin_wetter_vollständig_03_2026.csv","h1_color_light":"#1d6b2e","h1_color_dark":"#82e0aa","strahlung_colorscale":"Greens","bar_voll_color":"#27ae60","bar_aktuell_color":"#82e0aa","precip_color":"#1d6b2e","temp_cold_threshold":5,"temp_hot_threshold":18,"temp_colors":["#3498db","#27ae60","#f39c12"]},
    "Canberra":    {"filename":"csv/canberra_wetter_vollständig_03_2026.csv","h1_color_light":"#1a6b3c","h1_color_dark":"#76d7a0","strahlung_colorscale":"YlGn","bar_voll_color":"#229954","bar_aktuell_color":"#76d7a0","precip_color":"#1a6b3c","temp_cold_threshold":10,"temp_hot_threshold":28,"temp_colors":["#3498db","#f39c12","#e74c3c"]},
    "Wellington":  {"filename":"csv/wellington_wetter_vollständig_03_2026.csv","h1_color_light":"#154360","h1_color_dark":"#7fb3d3","strahlung_colorscale":"Blues","bar_voll_color":"#1f618d","bar_aktuell_color":"#7fb3d3","precip_color":"#154360","temp_cold_threshold":8,"temp_hot_threshold":20,"temp_colors":["#3498db","#27ae60","#f39c12"]},
    "Kapstadt":    {"filename":"csv/kapstadt_wetter_vollständig_03_2026.csv","h1_color_light":"#6c3483","h1_color_dark":"#c39bd3","strahlung_colorscale":"Purples","bar_voll_color":"#8e44ad","bar_aktuell_color":"#c39bd3","precip_color":"#5b2c6f","temp_cold_threshold":12,"temp_hot_threshold":25,"temp_colors":["#3498db","#f39c12","#e74c3c"]},
    "Rio":         {"filename":"csv/rio_wetter_vollständig_03_2026.csv","h1_color_light":"#1d6a2e","h1_color_dark":"#58d68d","strahlung_colorscale":"YlGn","bar_voll_color":"#27ae60","bar_aktuell_color":"#a9dfbf","precip_color":"#1a5276","temp_cold_threshold":20,"temp_hot_threshold":30,"temp_colors":["#f39c12","#e74c3c","#7b241c"]},
}

KONTINENTE = {
    "Europa":      ["Wien","Rom","Lissabon","Oslo","Dublin"],
    "Afrika":      ["Casablanca","Lagos","Nairobi","Kapstadt"],
    "Asien":       ["Medina","Mumbai","Shanghai","Tokyo","Yakutsk"],
    "Nordamerika": ["Las Vegas","Los Angeles","New York"],
    "Südamerika":  ["Santiago","Rio"],
    "Ozeanien":    ["Canberra","Wellington"],
}

KOORDINATEN = {
    "Wien":(48.2082,16.3738),"Casablanca":(33.5731,-7.5898),"Medina":(24.5247,39.5692),
    "Rom":(41.9028,12.4964),"Lissabon":(38.7223,-9.1393),"Santiago":(-33.4489,-70.6693),
    "Los Angeles":(34.0522,-118.2437),"Las Vegas":(36.1699,-115.1398),"New York":(40.7128,-74.0060),
    "Oslo":(59.9139,10.7522),"Tokyo":(35.6762,139.6503),"Shanghai":(31.2304,121.4737),
    "Mumbai":(19.0760,72.8777),"Dublin":(53.3498,-6.2603),"Canberra":(-35.2809,149.1300),
    "Wellington":(-41.2866,174.7756),"Yakutsk":(62.0355,129.6755),"Lagos":(6.5244,3.3792),
    "Nairobi":(-1.2921,36.8219),"Kapstadt":(-33.9249,18.4241),"Rio":(-22.9068,-43.1729),
}

MONAT_NAMEN_LIST = [MONATSNAMEN[i] for i in range(1, 13)]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sample_colorscale(scale_name: str, n: int = 12) -> list[str]:
    """Return n evenly-spaced hex/rgb colors from a plotly sequential colorscale."""
    try:
        palette = getattr(px.colors.sequential, scale_name)
    except AttributeError:
        palette = px.colors.sequential.Viridis

    if len(palette) >= n:
        # Even-spaced sampling
        indices = [int(round(i * (len(palette) - 1) / (n - 1))) for i in range(n)]
        return [palette[i] for i in indices]

    # Fewer entries than needed – interpolate using plotly's built-in sampler
    colors = px.colors.sample_colorscale(scale_name, [i / (n - 1) for i in range(n)])
    return colors


def df_to_records(df, round_cols: dict | None = None) -> list:
    """Convert a DataFrame to a list of plain dicts, rounding specified columns."""
    out = df.copy()
    if round_cols:
        for col, dec in round_cols.items():
            if col in out.columns:
                out[col] = out[col].round(dec)
    # Convert any Timestamp / Period columns to strings
    for col in out.columns:
        if hasattr(out[col], "dt"):
            out[col] = out[col].astype(str)
    return out.to_dict(orient="records")


# ---------------------------------------------------------------------------
# Main data collection
# ---------------------------------------------------------------------------

def collect_city_data() -> dict:
    all_data = {}
    for city, cfg in STAEDTE.items():
        csv_path = PROJECT_ROOT / cfg["filename"]
        try:
            d = load_data(str(csv_path))
        except FileNotFoundError:
            print(f"  SKIP {city} – CSV not found: {csv_path}")
            continue

        print(f"  OK   {city}")

        monthly = d["monthly"].copy()
        monthly["Datum"] = monthly["Datum"].dt.strftime("%Y-%m")

        monatsmittel = d["monatsmittel"].copy()
        jaehrlich = d["jaehrlich"].copy()
        temp_monatlich = d["temp_monatlich"].copy()
        temp_mittel = d["temp_mittel"].copy()
        precip_monatlich = d["precip_monatlich"].copy()
        precip_mittel = d["precip_mittel"].copy()
        temp_jaehrlich = d["temp_jaehrlich"].copy()
        precip_jaehrlich = d["precip_jaehrlich"].copy()

        all_data[city] = {
            "monthly": df_to_records(monthly, {"kWh_Tag": 2}),
            "monatsmittel": df_to_records(monatsmittel, {"kWh_Mittel": 2}),
            "jaehrlich": df_to_records(jaehrlich, {"kWh_Jahr": 1}),
            "temp_monatlich": df_to_records(temp_monatlich, {"Temp_Avg": 2}),
            "temp_mittel": df_to_records(temp_mittel, {"Temp_Avg": 2}),
            "precip_monatlich": df_to_records(precip_monatlich, {"Niederschlag_Tag": 2}),
            "precip_mittel": df_to_records(precip_mittel, {"Niederschlag_Tag": 2}),
            "temp_jaehrlich": df_to_records(temp_jaehrlich, {"Temp_Jahr": 3}),
            "precip_jaehrlich": df_to_records(precip_jaehrlich, {"Precip_Jahr": 1}),
            "alle_jahre": [int(j) for j in d["alle_jahre"]],
            "strahlung_colors": sample_colorscale(cfg["strahlung_colorscale"], 12),
        }

    return all_data


def build_staedte_js() -> dict:
    """Strip filename, keep everything else for JS config."""
    out = {}
    for city, cfg in STAEDTE.items():
        out[city] = {k: v for k, v in cfg.items() if k != "filename"}
    return out


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Wetter-Dashboard – Weltweiter Vergleich</title>
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js" charset="utf-8"></script>
<style>
  /* ── Reset & base ─────────────────────────────────────────── */
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:         #ffffff;
    --surface:    #f4f6f9;
    --border:     #dde2ea;
    --text:       #2c3e50;
    --text-muted: #6c7a8d;
    --accent:     #2471a3;
    --radius:     10px;
    --shadow:     0 2px 12px rgba(0,0,0,.08);
    --h1:         #2c3e50;
    --plot-bg:    white;
    --paper-bg:   white;
    --grid:       #eeeeee;
    --ann-bg:     rgba(255,255,255,0.90);
  }
  body.dark {
    --bg:         #111420;
    --surface:    #151823;
    --border:     #2a2f45;
    --text:       #e0e0e0;
    --text-muted: #8892a4;
    --accent:     #85c1e9;
    --h1:         #aed6f1;
    --plot-bg:    #1e2130;
    --paper-bg:   #151823;
    --grid:       #2e3347;
    --ann-bg:     rgba(21,24,35,0.92);
  }

  body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    transition: background .3s, color .3s;
    min-height: 100vh;
  }

  /* ── Layout shell ─────────────────────────────────────────── */
  #app {
    max-width: 1400px;
    margin: 0 auto;
    padding: 16px 20px 40px;
  }

  /* ── Top bar ──────────────────────────────────────────────── */
  #top-bar {
    display: flex;
    gap: 20px;
    align-items: flex-start;
    flex-wrap: wrap;
    margin-bottom: 18px;
  }

  #controls {
    flex: 0 0 auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-width: 280px;
  }

  #city-title {
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--h1);
    transition: color .3s;
    line-height: 1.2;
    margin-bottom: 2px;
  }

  .ctrl-row {
    display: flex;
    gap: 8px;
    align-items: center;
    flex-wrap: wrap;
  }

  label.ctrl-label {
    font-size: .8rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: .04em;
    min-width: 72px;
  }

  select {
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 5px 10px;
    font-size: .9rem;
    cursor: pointer;
    outline: none;
    transition: border-color .2s, background .3s, color .3s;
    appearance: none;
    -webkit-appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%236c7a8d' stroke-width='1.8' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 10px center;
    padding-right: 30px;
  }
  select:focus { border-color: var(--accent); }

  #map-section {
    flex: 1 1 380px;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 8px;
  }

  #theme-toggle {
    align-self: flex-end;
    background: #2c3e50;
    color: #fff;
    border: none;
    border-radius: 20px;
    padding: 6px 16px;
    font-size: .85rem;
    cursor: pointer;
    transition: background .3s, color .3s;
    font-weight: 600;
  }
  body.dark #theme-toggle {
    background: #e0e0e0;
    color: #151823;
  }

  #world-map {
    width: 100%;
    height: 200px;
    border-radius: var(--radius);
    overflow: hidden;
    border: 1px solid var(--border);
  }

  /* ── Main chart ───────────────────────────────────────────── */
  #chart-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: var(--shadow);
    transition: background .3s, border-color .3s;
  }

  #main-chart {
    width: 100%;
    height: 520px;
  }

  /* ── Year selector (shown only for certain views) ─────────── */
  #year-row {
    display: none;
  }
  #year-row.visible {
    display: flex;
  }

  /* ── Responsive ───────────────────────────────────────────── */
  @media (max-width: 720px) {
    #top-bar { flex-direction: column; }
    #map-section { align-items: stretch; width: 100%; }
    #world-map { height: 160px; }
    #main-chart { height: 380px; }
  }
</style>
</head>
<body>
<div id="app">

  <!-- Top bar -->
  <div id="top-bar">

    <!-- Left: controls -->
    <div id="controls">
      <div id="city-title">Wien</div>

      <div class="ctrl-row">
        <label class="ctrl-label" for="sel-kontinent">Kontinent</label>
        <select id="sel-kontinent"></select>
      </div>

      <div class="ctrl-row">
        <label class="ctrl-label" for="sel-stadt">Stadt</label>
        <select id="sel-stadt"></select>
      </div>

      <div class="ctrl-row">
        <label class="ctrl-label" for="sel-ansicht">Ansicht</label>
        <select id="sel-ansicht">
          <option value="jahresverlauf">Strahlung nach Jahr</option>
          <option value="zeitreihe">Strahlung Zeitreihe</option>
          <option value="jahressummen">Strahlung Jahressummen</option>
          <option value="temperaturen">Temperaturen</option>
          <option value="niederschlag">Niederschlag</option>
          <option value="temp_trend">Temp. Jahrestrend</option>
          <option value="precip_trend">Niederschlag Jahrestrend</option>
        </select>
      </div>

      <div class="ctrl-row" id="year-row">
        <label class="ctrl-label" for="sel-jahr">Jahr</label>
        <select id="sel-jahr"></select>
      </div>
    </div>

    <!-- Right: toggle + map -->
    <div id="map-section">
      <button id="theme-toggle">🌙 Dark</button>
      <div id="world-map"></div>
    </div>

  </div><!-- /top-bar -->

  <!-- Main chart -->
  <div id="chart-container">
    <div id="main-chart"></div>
  </div>

</div><!-- /app -->

<script>
// ============================================================
// Embedded data
// ============================================================
const CITY_DATA   = __CITY_DATA__;
const STAEDTE_CFG = __STAEDTE_CFG__;
const KONTINENTE  = __KONTINENTE__;
const KOORDINATEN = __KOORDINATEN__;
const MONAT_NAMEN = __MONAT_NAMEN__;

// ============================================================
// State
// ============================================================
let currentCity   = Object.keys(KONTINENTE[Object.keys(KONTINENTE)[0]])[0];
let currentTheme  = 'light';
let isDark        = false;

// Initialize first city to first continent's first city
(function initFirstCity() {
  const firstKont = Object.keys(KONTINENTE)[0];
  currentCity = KONTINENTE[firstKont][0];
})();

// ============================================================
// Theme helpers
// ============================================================
const THEMES = {
  light: { plot_bg:'white', paper_bg:'white', grid:'#eeeeee', font:'#2c3e50', ann_bg:'rgba(255,255,255,0.90)' },
  dark:  { plot_bg:'#1e2130', paper_bg:'#151823', grid:'#2e3347', font:'#e0e0e0', ann_bg:'rgba(21,24,35,0.92)' },
};

function theme() { return THEMES[isDark ? 'dark' : 'light']; }

// ============================================================
// Utilities
// ============================================================
function polyfit(xs, ys) {
  // Simple linear regression, returns {slope, intercept}
  const n = xs.length;
  if (n < 2) return { slope: 0, intercept: ys[0] || 0 };
  let sumX=0, sumY=0, sumXY=0, sumXX=0;
  for (let i=0; i<n; i++) { sumX+=xs[i]; sumY+=ys[i]; sumXY+=xs[i]*ys[i]; sumXX+=xs[i]*xs[i]; }
  const slope = (n*sumXY - sumX*sumY) / (n*sumXX - sumX*sumX);
  const intercept = (sumY - slope*sumX) / n;
  return { slope, intercept };
}

function mean(arr) { return arr.reduce((a,b)=>a+b,0)/arr.length; }

function round(v, dec) { return Math.round(v * Math.pow(10,dec)) / Math.pow(10,dec); }

function cityData() { return CITY_DATA[currentCity]; }
function cityCfg()  { return STAEDTE_CFG[currentCity]; }

function h1Color() {
  const cfg = cityCfg();
  return isDark ? cfg.h1_color_dark : cfg.h1_color_light;
}

// ============================================================
// Plotly layout defaults
// ============================================================
function baseLayout(extra) {
  const t = theme();
  return Object.assign({
    paper_bgcolor: t.paper_bg,
    plot_bgcolor:  t.plot_bg,
    font: { color: t.font, family: "'Segoe UI', system-ui, sans-serif" },
    margin: { t: 50, r: 20, b: 60, l: 60 },
    yaxis: { gridcolor: t.grid, zerolinecolor: t.grid },
    xaxis: { gridcolor: t.grid, zerolinecolor: t.grid },
    legend: { orientation:'h', y:1.05 },
    transition: { duration: 300 },
  }, extra);
}

function annotationStyle(text) {
  const t = theme();
  return {
    x:0.02, y:0.97, xref:'paper', yref:'paper', showarrow:false,
    text,
    font: { size:13, color:'#c0392b' },
    bgcolor: t.ann_bg,
    borderpad: 6,
  };
}

// ============================================================
// Chart renderers
// ============================================================

function renderJahresverlauf() {
  const d   = cityData();
  const cfg = cityCfg();
  const sel = document.getElementById('sel-jahr').value;
  const colors = d.strahlung_colors;  // 12 colors

  let x, y, title;
  if (sel === 'alle') {
    x     = d.monatsmittel.map(r => r.MonatName);
    y     = d.monatsmittel.map(r => r.kWh_Mittel);
    title = `Ø Solarenergie pro Monat – ${currentCity} (alle Jahre)`;
  } else {
    const yr = parseInt(sel);
    const rows = d.monthly.filter(r => parseInt(r.Jahr) === yr);
    x     = rows.map(r => MONAT_NAMEN[parseInt(r.Monat)-1]);
    y     = rows.map(r => r.kWh_Tag);
    title = `Solarenergie ${yr} – ${currentCity}, kWh/m² pro Monat`;
  }

  const traces = [{
    type: 'bar', x, y,
    marker: { color: colors },
    text: y.map(v => round(v,1)),
    textposition: 'outside',
    hovertemplate: '%{x}: %{y:.1f} kWh/m²<extra></extra>',
  }];
  const layout = baseLayout({ title: { text: title }, xaxis_title:'Monat', yaxis_title:'kWh/m²' });
  Plotly.react('main-chart', traces, layout, { responsive:true, displayModeBar:false });
}

function renderZeitreihe() {
  const d   = cityData();
  const cfg = cityCfg();
  const x   = d.monthly.map(r => r.Datum);
  const y   = d.monthly.map(r => r.kWh_Tag);
  const traces = [{
    type:'bar', x, y,
    marker: { color: cfg.bar_voll_color },
    hovertemplate: '%{x}: %{y:.1f} kWh/m²<extra></extra>',
  }];
  const layout = baseLayout({
    title: { text: `Monatliche Solarenergie – ${currentCity}, alle Jahre` },
    xaxis: { title:'Datum', rangeslider:{ visible:true }, gridcolor: theme().grid },
    yaxis_title: 'kWh/m²',
    margin: { t:50, r:20, b:100, l:60 },
  });
  Plotly.react('main-chart', traces, layout, { responsive:true, displayModeBar:false });
}

function renderJahressummen() {
  const d   = cityData();
  const cfg = cityCfg();
  const voll    = d.jaehrlich.filter(r => r.Jahr < 2026);
  const aktuell = d.jaehrlich.filter(r => r.Jahr >= 2026);
  const mittel  = mean(voll.map(r => r.kWh_Jahr));

  const traces = [];
  traces.push({
    type:'bar',
    x: voll.map(r=>r.Jahr), y: voll.map(r=>round(r.kWh_Jahr,0)),
    name:'Jahressumme',
    marker:{ color: cfg.bar_voll_color },
    text: voll.map(r=>Math.round(r.kWh_Jahr)),
    textposition:'outside', textfont:{size:9},
    hovertemplate:'%{x}: %{y:.0f} kWh/m²<extra></extra>',
  });
  if (aktuell.length) {
    traces.push({
      type:'bar',
      x: aktuell.map(r=>r.Jahr), y: aktuell.map(r=>round(r.kWh_Jahr,0)),
      name:'2026 (unvollständig)',
      marker:{ color: cfg.bar_aktuell_color, pattern:{ shape:'/', solidity:0.3 } },
      text: aktuell.map(r=>Math.round(r.kWh_Jahr)),
      textposition:'outside', textfont:{size:9},
      hovertemplate:'%{x}: %{y:.0f} kWh/m² (bis März)<extra></extra>',
    });
  }

  const allX = d.jaehrlich.map(r=>r.Jahr);
  traces.push({
    type:'scatter', mode:'lines',
    x:[Math.min(...allX), Math.max(...allX)],
    y:[mittel, mittel],
    name:`Ø ${Math.round(mittel)} kWh/m²`,
    line:{ color:'#c0392b', dash:'dash', width:2 },
    hoverinfo:'skip',
  });

  const layout = baseLayout({
    title:{ text:`Gesamte Solarenergie pro Jahr – ${currentCity}` },
    xaxis:{ title:'Jahr', dtick:1, tickangle:-45, gridcolor:theme().grid },
    yaxis:{ title:'kWh/m²', gridcolor:theme().grid },
    bargap:0.15,
  });
  Plotly.react('main-chart', traces, layout, { responsive:true, displayModeBar:false });
}

function renderTemperaturen() {
  const d   = cityData();
  const cfg = cityCfg();
  const sel = document.getElementById('sel-jahr').value;

  let x, y, title;
  if (sel === 'alle') {
    x     = d.temp_mittel.map(r => r.MonatName);
    y     = d.temp_mittel.map(r => r.Temp_Avg);
    title = `Ø Monatstemperatur – ${currentCity} (alle Jahre)`;
  } else {
    const yr = parseInt(sel);
    const rows = d.temp_monatlich.filter(r => r.Jahr === yr);
    x     = rows.map(r => MONAT_NAMEN[r.Monat-1]);
    y     = rows.map(r => r.Temp_Avg);
    title = `Monatstemperatur ${yr} – ${currentCity}`;
  }

  const [cold_c, mid_c, hot_c] = cfg.temp_colors;
  const colors = y.map(v =>
    v < cfg.temp_cold_threshold ? cold_c :
    v > cfg.temp_hot_threshold  ? hot_c  : mid_c
  );
  const avg = mean(y);

  const traces = [
    {
      type:'bar', x, y,
      marker:{ color: colors },
      text: y.map(v=>round(v,1)), textposition:'outside',
      hovertemplate:'%{x}: %{y:.1f} °C<extra></extra>',
    },
    // Mean line
    { type:'scatter', mode:'lines', x:[x[0], x[x.length-1]], y:[avg,avg],
      name:`Ø ${round(avg,1)} °C`, line:{color:'#8e44ad', dash:'dash', width:2}, hoverinfo:'skip' },
  ];
  if (cfg.temp_cold_threshold <= 0) {
    traces.push({ type:'scatter', mode:'lines', x:[x[0],x[x.length-1]], y:[0,0],
      line:{color:'#aaaaaa', width:1}, hoverinfo:'skip', showlegend:false });
  }

  const layout = baseLayout({
    title:{ text: title },
    xaxis:{ title:'Monat', gridcolor:theme().grid },
    yaxis:{ title:'°C', gridcolor:theme().grid },
  });
  Plotly.react('main-chart', traces, layout, { responsive:true, displayModeBar:false });
}

function renderNiederschlag() {
  const d   = cityData();
  const cfg = cityCfg();
  const sel = document.getElementById('sel-jahr').value;

  let x, y, title, annotation_text;
  if (sel === 'alle') {
    x     = d.precip_mittel.map(r => r.MonatName);
    y     = d.precip_mittel.map(r => r.Niederschlag_Tag);
    title = `Ø Monatsniederschlag – ${currentCity} (alle Jahre)`;
    const jahressumme = mean(
      Object.values(
        d.precip_monatlich.reduce((acc, r) => {
          acc[r.Jahr] = (acc[r.Jahr]||0) + r.Niederschlag_Tag;
          return acc;
        }, {})
      )
    );
    annotation_text = `Ø Jahressumme: ${Math.round(jahressumme)} mm`;
  } else {
    const yr = parseInt(sel);
    const rows = d.precip_monatlich.filter(r => r.Jahr === yr);
    x     = rows.map(r => MONAT_NAMEN[r.Monat-1]);
    y     = rows.map(r => r.Niederschlag_Tag);
    title = `Monatsniederschlag ${yr} – ${currentCity}`;
    annotation_text = `Jahressumme: ${Math.round(y.reduce((a,b)=>a+b,0))} mm`;
  }

  const traces = [{
    type:'bar', x, y,
    marker:{ color: cfg.precip_color },
    text: y.map(v=>round(v,1)), textposition:'outside',
    hovertemplate:'%{x}: %{y:.1f} mm<extra></extra>',
  }];

  const layout = baseLayout({
    title:{ text: title },
    xaxis:{ title:'Monat', gridcolor:theme().grid },
    yaxis:{ title:'mm', gridcolor:theme().grid },
    annotations:[ annotationStyle(annotation_text) ],
  });
  Plotly.react('main-chart', traces, layout, { responsive:true, displayModeBar:false });
}

function renderTempTrend() {
  const d   = cityData();
  const cfg = cityCfg();
  const rows = d.temp_jaehrlich.filter(r => r.Jahr < 2026);
  const xs   = rows.map(r => r.Jahr);
  const ys   = rows.map(r => r.Temp_Jahr);
  const { slope, intercept } = polyfit(xs, ys);
  const trendDekade = slope * 10;
  const fitY = xs.map(x => round(slope*x + intercept, 3));
  const arrow = trendDekade > 0 ? '▲' : '▼';

  const traces = [
    {
      type:'scatter', mode:'lines+markers', x:xs, y:ys.map(v=>round(v,2)),
      name:'Jahresmittel',
      line:{ color: cfg.bar_voll_color, width:2 },
      marker:{ size:6 },
      hovertemplate:'%{x}: %{y:.2f} °C<extra></extra>',
    },
    {
      type:'scatter', mode:'lines', x:xs, y:fitY,
      name:`Linearer Trend (${trendDekade>=0?'+':''}${round(trendDekade,3)} °C/Dekade)`,
      line:{ color:'#e74c3c', width:2, dash:'dash' },
    },
  ];
  const layout = baseLayout({
    title:{ text:`Jährliche Durchschnittstemperatur – ${currentCity}` },
    xaxis:{ title:'Jahr', dtick:5, gridcolor:theme().grid },
    yaxis:{ title:'°C', gridcolor:theme().grid },
    annotations:[{
      x:0.02, y:0.95, xref:'paper', yref:'paper', showarrow:false,
      text:`${arrow} <b>${Math.abs(round(trendDekade,3))} °C pro Dekade</b>`,
      font:{ size:14, color:'#e74c3c' },
      bgcolor: theme().ann_bg,
      borderpad:8,
    }],
  });
  Plotly.react('main-chart', traces, layout, { responsive:true, displayModeBar:false });
}

function renderPrecipTrend() {
  const d   = cityData();
  const cfg = cityCfg();
  const rows = d.precip_jaehrlich.filter(r => r.Jahr < 2026);
  const xs   = rows.map(r => r.Jahr);
  const ys   = rows.map(r => r.Precip_Jahr);
  const { slope, intercept } = polyfit(xs, ys);
  const trendDekade = slope * 10;
  const fitY = xs.map(x => round(slope*x + intercept, 1));
  const arrow = trendDekade > 0 ? '▲' : '▼';

  const traces = [
    {
      type:'bar', x:xs, y:ys.map(v=>round(v,1)),
      name:'Jahresniederschlag',
      marker:{ color: cfg.precip_color },
      hovertemplate:'%{x}: %{y:.0f} mm<extra></extra>',
    },
    {
      type:'scatter', mode:'lines', x:xs, y:fitY,
      name:`Linearer Trend (${trendDekade>=0?'+':''}${round(trendDekade,1)} mm/Dekade)`,
      line:{ color:'#e74c3c', width:2, dash:'dash' },
    },
  ];
  const layout = baseLayout({
    title:{ text:`Jährlicher Gesamtniederschlag – ${currentCity}` },
    xaxis:{ title:'Jahr', dtick:5, gridcolor:theme().grid },
    yaxis:{ title:'mm', gridcolor:theme().grid },
    annotations:[{
      x:0.02, y:0.95, xref:'paper', yref:'paper', showarrow:false,
      text:`${arrow} <b>${Math.abs(round(trendDekade,1))} mm pro Dekade</b>`,
      font:{ size:14, color:'#e74c3c' },
      bgcolor: theme().ann_bg,
      borderpad:8,
    }],
  });
  Plotly.react('main-chart', traces, layout, { responsive:true, displayModeBar:false });
}

// ============================================================
// World map
// ============================================================

function renderMap() {
  const t = theme();
  const cities = Object.keys(KOORDINATEN).filter(c => CITY_DATA[c]);
  const lats=[], lons=[], names=[], sizes=[], colors=[], borders=[];
  for (const c of cities) {
    const [lat, lon] = KOORDINATEN[c];
    lats.push(lat); lons.push(lon); names.push(c);
    const isSelected = c === currentCity;
    sizes.push(isSelected ? 12 : 7);
    colors.push(isSelected ? '#e74c3c' : '#2471a3');
    borders.push(isSelected ? 'white' : 'rgba(255,255,255,0.5)');
  }
  const traces = [{
    type:'scattergeo', lat:lats, lon:lons, text:names, mode:'markers',
    hovertemplate:'%{text}<extra></extra>',
    marker:{
      size: sizes,
      color: colors,
      line:{ color: borders, width: sizes.map(s => s>8?2:1) },
    },
  }];
  const layout = {
    paper_bgcolor: t.paper_bg,
    margin:{ t:0, r:0, b:0, l:0 },
    geo:{
      projection:{ type:'natural earth' },
      bgcolor: t.paper_bg,
      landcolor: isDark ? '#2a3550' : '#dce9f5',
      oceancolor: isDark ? '#151e30' : '#c8dff5',
      lakecolor: isDark ? '#151e30' : '#c8dff5',
      coastlinecolor: isDark ? '#3a4a65' : '#aabbcc',
      countrycolor: isDark ? '#3a4a65' : '#aabbcc',
      showland:true, showocean:true, showlakes:true,
      showcountries:true,
    },
    showlegend:false,
    dragmode:false,
  };
  Plotly.react('world-map', traces, layout, { responsive:true, displayModeBar:false, scrollZoom:false });
}

// ============================================================
// Dropdown population
// ============================================================

function populateKontinente() {
  const sel = document.getElementById('sel-kontinent');
  sel.innerHTML = '';
  for (const k of Object.keys(KONTINENTE)) {
    const opt = document.createElement('option');
    opt.value = k; opt.textContent = k;
    sel.appendChild(opt);
  }
}

function populateStaedte(kontinent) {
  const sel = document.getElementById('sel-stadt');
  sel.innerHTML = '';
  for (const c of KONTINENTE[kontinent]) {
    if (!CITY_DATA[c]) continue;
    const opt = document.createElement('option');
    opt.value = c; opt.textContent = c;
    sel.appendChild(opt);
  }
}

function populateJahre() {
  const d   = cityData();
  const sel = document.getElementById('sel-jahr');
  const current = sel.value;
  sel.innerHTML = '<option value="alle">Ø alle Jahre</option>';
  for (const j of d.alle_jahre) {
    const opt = document.createElement('option');
    opt.value = j; opt.textContent = j;
    sel.appendChild(opt);
  }
  // Restore selection if still valid
  if ([...sel.options].some(o=>o.value===current)) sel.value = current;
  else sel.value = 'alle';
}

// ============================================================
// Routing
// ============================================================

const VIEWS_WITH_YEAR = new Set(['jahresverlauf','temperaturen','niederschlag']);

function render() {
  const view = document.getElementById('sel-ansicht').value;
  const yearRow = document.getElementById('year-row');
  yearRow.classList.toggle('visible', VIEWS_WITH_YEAR.has(view));

  switch(view) {
    case 'jahresverlauf': renderJahresverlauf(); break;
    case 'zeitreihe':     renderZeitreihe();     break;
    case 'jahressummen':  renderJahressummen();  break;
    case 'temperaturen':  renderTemperaturen();  break;
    case 'niederschlag':  renderNiederschlag();  break;
    case 'temp_trend':    renderTempTrend();     break;
    case 'precip_trend':  renderPrecipTrend();   break;
  }
}

function selectCity(city) {
  if (!CITY_DATA[city]) return;
  currentCity = city;

  // Sync continent dropdown
  for (const [k, cities] of Object.entries(KONTINENTE)) {
    if (cities.includes(city)) {
      document.getElementById('sel-kontinent').value = k;
      populateStaedte(k);
      break;
    }
  }
  document.getElementById('sel-stadt').value = city;
  populateJahre();

  // Update h1 color
  const titleEl = document.getElementById('city-title');
  titleEl.textContent = city;
  titleEl.style.color = h1Color();

  renderMap();
  render();
}

// ============================================================
// Theme toggle
// ============================================================

function applyTheme() {
  document.body.classList.toggle('dark', isDark);
  const btn = document.getElementById('theme-toggle');
  btn.textContent = isDark ? '☀️ Light' : '🌙 Dark';
  // Update h1 color
  const titleEl = document.getElementById('city-title');
  titleEl.style.color = h1Color();
  renderMap();
  render();
}

// ============================================================
// Event wiring
// ============================================================

document.getElementById('sel-kontinent').addEventListener('change', function() {
  populateStaedte(this.value);
  // Auto-select first available city in continent
  const first = document.getElementById('sel-stadt').value;
  selectCity(first);
});

document.getElementById('sel-stadt').addEventListener('change', function() {
  selectCity(this.value);
});

document.getElementById('sel-ansicht').addEventListener('change', function() {
  render();
});

document.getElementById('sel-jahr').addEventListener('change', function() {
  render();
});

document.getElementById('theme-toggle').addEventListener('click', function() {
  isDark = !isDark;
  applyTheme();
});

// Map click
document.getElementById('world-map').on('plotly_click', function(data) {
  if (!data || !data.points || !data.points.length) return;
  const city = data.points[0].text;
  selectCity(city);
});

// ============================================================
// Init
// ============================================================

(function init() {
  populateKontinente();

  // Find continent of default city
  let defaultKont = Object.keys(KONTINENTE)[0];
  for (const [k, cities] of Object.entries(KONTINENTE)) {
    if (cities.includes(currentCity)) { defaultKont = k; break; }
  }
  document.getElementById('sel-kontinent').value = defaultKont;
  populateStaedte(defaultKont);
  document.getElementById('sel-stadt').value = currentCity;
  populateJahre();

  const titleEl = document.getElementById('city-title');
  titleEl.textContent = currentCity;
  titleEl.style.color = h1Color();

  renderMap();
  render();
})();
</script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    print("Collecting city data…")
    city_data = collect_city_data()

    if not city_data:
        print("ERROR: No city data loaded. Check that CSV files exist in csv/.")
        sys.exit(1)

    print(f"\nLoaded {len(city_data)} cities. Building HTML…")

    # Serialize embedded blobs
    city_data_json    = json.dumps(city_data, ensure_ascii=False, separators=(',', ':'))
    staedte_cfg_json  = json.dumps(build_staedte_js(), ensure_ascii=False, separators=(',', ':'))
    kontinente_json   = json.dumps(KONTINENTE, ensure_ascii=False, separators=(',', ':'))
    koordinaten_json  = json.dumps(
        {k: list(v) for k, v in KOORDINATEN.items()},
        ensure_ascii=False, separators=(',', ':')
    )
    monat_namen_json  = json.dumps(MONAT_NAMEN_LIST, ensure_ascii=False, separators=(',', ':'))

    html = HTML_TEMPLATE \
        .replace('__CITY_DATA__',   city_data_json) \
        .replace('__STAEDTE_CFG__', staedte_cfg_json) \
        .replace('__KONTINENTE__',  kontinente_json) \
        .replace('__KOORDINATEN__', koordinaten_json) \
        .replace('__MONAT_NAMEN__', monat_namen_json)

    out_path = PROJECT_ROOT / "dashboard.html"
    out_path.write_text(html, encoding="utf-8")
    size_kb = out_path.stat().st_size / 1024
    print(f"Written: {out_path}  ({size_kb:.0f} kB)")


if __name__ == "__main__":
    main()
