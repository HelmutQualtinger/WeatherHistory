import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, State

from weather_dash_lib import load_data, MONATSNAMEN
import webbrowser

# ---------------------------------------------------------------------------
# Themes
# ---------------------------------------------------------------------------
THEMES = {
    "light": {
        "plot_bg":      "white",
        "paper_bg":     "white",
        "grid":         "#eeeeee",
        "font":         "#2c3e50",
        "container_bg": "#ffffff",
        "toggle_label": "🌙 Dark",
        "toggle_bg":    "#2c3e50",
        "toggle_fg":    "#ffffff",
        "tab_bg":       "#f9f9f9",
        "tab_sel_bg":   "#ffffff",
        "tab_border":   "#d0d0d0",
        "ann_bg":       "rgba(255,255,255,0.85)",
        "ann_border":   "#444444",
    },
    "dark": {
        "plot_bg":      "#1e2130",
        "paper_bg":     "#151823",
        "grid":         "#2e3347",
        "font":         "#e0e0e0",
        "container_bg": "#151823",
        "toggle_label": "☀️ Light",
        "toggle_bg":    "#e0e0e0",
        "toggle_fg":    "#151823",
        "tab_bg":       "#1e2130",
        "tab_sel_bg":   "#2a2f45",
        "tab_border":   "#2e3347",
        "ann_bg":       "rgba(30,33,48,0.92)",
    },
}

# ---------------------------------------------------------------------------
# Stadtkonfigurationen
# ---------------------------------------------------------------------------
STAEDTE = {
    "Wien": {
        "filename": "csv/wien_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#2c3e50",
        "h1_color_dark":           "#aed6f1",
        "strahlung_colorscale":    "YlOrRd",
        "bar_voll_color":          "#e67e22",
        "bar_aktuell_color":       "#f39c12",
        "precip_color":            "#2980b9",
        "temp_cold_threshold":     0,
        "temp_hot_threshold":      20,
        "temp_colors":             ["#3498db", "#f39c12", "#e74c3c"],
    },
    "Lagos": {
        "filename": "csv/lagos_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#117a65",
        "h1_color_dark":           "#76d7c4",
        "strahlung_colorscale":    "YlOrRd",
        "bar_voll_color":          "#d35400",
        "bar_aktuell_color":       "#f0b27a",
        "precip_color":            "#1a5276",
        "temp_cold_threshold":     22,
        "temp_hot_threshold":      32,
        "temp_colors":             ["#f39c12", "#e74c3c", "#7b241c"],
    },
    "Nairobi": {
        "filename": "csv/nairobi_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#1e6b3c",
        "h1_color_dark":           "#82e0aa",
        "strahlung_colorscale":    "YlGn",
        "bar_voll_color":          "#27ae60",
        "bar_aktuell_color":       "#82e0aa",
        "precip_color":            "#1e6b3c",
        "temp_cold_threshold":     15,
        "temp_hot_threshold":      28,
        "temp_colors":             ["#3498db", "#f39c12", "#e74c3c"],
    },
    "Casablanca": {
        "filename": "csv/casablanca_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#1a5276",
        "h1_color_dark":           "#7fb3d3",
        "strahlung_colorscale":    "solar",
        "bar_voll_color":          "#2980b9",
        "bar_aktuell_color":       "#85c1e9",
        "precip_color":            "#1a5276",
        "temp_cold_threshold":     15,
        "temp_hot_threshold":      28,
        "temp_colors":             ["#3498db", "#f39c12", "#e74c3c"],
    },
    "Medina": {
        "filename": "csv/medina_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#6e2f00",
        "h1_color_dark":           "#e59866",
        "strahlung_colorscale":    "Oranges",
        "bar_voll_color":          "#c0392b",
        "bar_aktuell_color":       "#e59866",
        "precip_color":            "#c0392b",
        "temp_cold_threshold":     25,
        "temp_hot_threshold":      35,
        "temp_colors":             ["#f39c12", "#c0392b", "#7b241c"],
    },
    "Rom": {
        "filename": "csv/rome_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#7b241c",
        "h1_color_dark":           "#f1948a",
        "strahlung_colorscale":    "Reds",
        "bar_voll_color":          "#c0392b",
        "bar_aktuell_color":       "#e59866",
        "precip_color":            "#7b241c",
        "temp_cold_threshold":     5,
        "temp_hot_threshold":      25,
        "temp_colors":             ["#3498db", "#f39c12", "#e74c3c"],
    },
    "Lissabon": {
        "filename": "csv/lisbon_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#1a6b8a",
        "h1_color_dark":           "#76d7c4",
        "strahlung_colorscale":    "Blues",
        "bar_voll_color":          "#2471a3",
        "bar_aktuell_color":       "#7fb3d3",
        "precip_color":            "#1a6b8a",
        "temp_cold_threshold":     10,
        "temp_hot_threshold":      25,
        "temp_colors":             ["#3498db", "#f39c12", "#e74c3c"],
    },
    "Santiago": {
        "filename": "csv/santiago_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#6c3483",
        "h1_color_dark":           "#d2b4de",
        "strahlung_colorscale":    "Purples",
        "bar_voll_color":          "#7d3c98",
        "bar_aktuell_color":       "#d2b4de",
        "precip_color":            "#6c3483",
        "temp_cold_threshold":     10,
        "temp_hot_threshold":      25,
        "temp_colors":             ["#3498db", "#f39c12", "#e74c3c"],
    },
    "Las Vegas": {
        "filename": "csv/lasvegas_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#7d6608",
        "h1_color_dark":           "#f7dc6f",
        "strahlung_colorscale":    "YlOrRd",
        "bar_voll_color":          "#d4ac0d",
        "bar_aktuell_color":       "#f9e79f",
        "precip_color":            "#7d6608",
        "temp_cold_threshold":     10,
        "temp_hot_threshold":      35,
        "temp_colors":             ["#3498db", "#f39c12", "#e74c3c"],
    },
    "Los Angeles": {
        "filename": "csv/losangeles_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#b7950b",
        "h1_color_dark":           "#f9e79f",
        "strahlung_colorscale":    "YlOrBr",
        "bar_voll_color":          "#d4ac0d",
        "bar_aktuell_color":       "#f9e79f",
        "precip_color":            "#b7950b",
        "temp_cold_threshold":     12,
        "temp_hot_threshold":      28,
        "temp_colors":             ["#3498db", "#f39c12", "#e74c3c"],
    },
    "New York": {
        "filename": "csv/newyork_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#1a3a5c",
        "h1_color_dark":           "#85c1e9",
        "strahlung_colorscale":    "Blues",
        "bar_voll_color":          "#2471a3",
        "bar_aktuell_color":       "#85c1e9",
        "precip_color":            "#1a3a5c",
        "temp_cold_threshold":     0,
        "temp_hot_threshold":      25,
        "temp_colors":             ["#3498db", "#f39c12", "#e74c3c"],
    },
    "Oslo": {
        "filename": "csv/oslo_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#117a65",
        "h1_color_dark":           "#76d7c4",
        "strahlung_colorscale":    "BuGn",
        "bar_voll_color":          "#148f77",
        "bar_aktuell_color":       "#76d7c4",
        "precip_color":            "#117a65",
        "temp_cold_threshold":     0,
        "temp_hot_threshold":      18,
        "temp_colors":             ["#3498db", "#f39c12", "#e74c3c"],
    },
    "Yakutsk": {
        "filename": "csv/yakutsk_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#1a3a5c",
        "h1_color_dark":           "#aed6f1",
        "strahlung_colorscale":    "Blues",
        "bar_voll_color":          "#2471a3",
        "bar_aktuell_color":       "#aed6f1",
        "precip_color":            "#1a3a5c",
        "temp_cold_threshold":     -30,
        "temp_hot_threshold":      15,
        "temp_colors":             ["#3498db", "#f39c12", "#e74c3c"],
    },
    "Tokyo": {
        "filename": "csv/tokyo_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#1b4f8a",
        "h1_color_dark":           "#85c1e9",
        "strahlung_colorscale":    "Blues",
        "bar_voll_color":          "#2471a3",
        "bar_aktuell_color":       "#85c1e9",
        "precip_color":            "#1b4f8a",
        "temp_cold_threshold":     5,
        "temp_hot_threshold":      25,
        "temp_colors":             ["#3498db", "#f39c12", "#e74c3c"],
    },
    "Shanghai": {
        "filename": "csv/shanghai_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#922b21",
        "h1_color_dark":           "#f1948a",
        "strahlung_colorscale":    "Reds",
        "bar_voll_color":          "#c0392b",
        "bar_aktuell_color":       "#f1948a",
        "precip_color":            "#922b21",
        "temp_cold_threshold":     5,
        "temp_hot_threshold":      28,
        "temp_colors":             ["#3498db", "#f39c12", "#e74c3c"],
    },
    "Mumbai": {
        "filename": "csv/mumbai_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#784212",
        "h1_color_dark":           "#f0b27a",
        "strahlung_colorscale":    "Oranges",
        "bar_voll_color":          "#ca6f1e",
        "bar_aktuell_color":       "#f0b27a",
        "precip_color":            "#1a5276",
        "temp_cold_threshold":     20,
        "temp_hot_threshold":      32,
        "temp_colors":             ["#f39c12", "#e74c3c", "#7b241c"],
    },
    "Dublin": {
        "filename": "csv/dublin_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#1d6b2e",
        "h1_color_dark":           "#82e0aa",
        "strahlung_colorscale":    "Greens",
        "bar_voll_color":          "#27ae60",
        "bar_aktuell_color":       "#82e0aa",
        "precip_color":            "#1d6b2e",
        "temp_cold_threshold":     5,
        "temp_hot_threshold":      18,
        "temp_colors":             ["#3498db", "#27ae60", "#f39c12"],
    },
    "Canberra": {
        "filename": "csv/canberra_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#1a6b3c",
        "h1_color_dark":           "#76d7a0",
        "strahlung_colorscale":    "YlGn",
        "bar_voll_color":          "#229954",
        "bar_aktuell_color":       "#76d7a0",
        "precip_color":            "#1a6b3c",
        "temp_cold_threshold":     10,
        "temp_hot_threshold":      28,
        "temp_colors":             ["#3498db", "#f39c12", "#e74c3c"],
    },
    "Wellington": {
        "filename": "csv/wellington_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#154360",
        "h1_color_dark":           "#7fb3d3",
        "strahlung_colorscale":    "Blues",
        "bar_voll_color":          "#1f618d",
        "bar_aktuell_color":       "#7fb3d3",
        "precip_color":            "#154360",
        "temp_cold_threshold":     8,
        "temp_hot_threshold":      20,
        "temp_colors":             ["#3498db", "#27ae60", "#f39c12"],
    },
    "Kapstadt": {
        "filename":                "csv/kapstadt_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#6c3483",
        "h1_color_dark":           "#c39bd3",
        "strahlung_colorscale":    "Purples",
        "bar_voll_color":          "#8e44ad",
        "bar_aktuell_color":       "#c39bd3",
        "precip_color":            "#5b2c6f",
        "temp_cold_threshold":     12,
        "temp_hot_threshold":      25,
        "temp_colors":             ["#3498db", "#f39c12", "#e74c3c"],
    },
    "Rio": {
        "filename":                "csv/rio_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#1d6a2e",
        "h1_color_dark":           "#58d68d",
        "strahlung_colorscale":    "YlGn",
        "bar_voll_color":          "#27ae60",
        "bar_aktuell_color":       "#a9dfbf",
        "precip_color":            "#1a5276",
        "temp_cold_threshold":     20,
        "temp_hot_threshold":      30,
        "temp_colors":             ["#f39c12", "#e74c3c", "#7b241c"],
    },
    "Kuala Lumpur": {
        "filename":                "csv/kualalumpur_wetter_vollständig_03_2026.csv",
        "h1_color_light":          "#0e6655",
        "h1_color_dark":           "#76d7c4",
        "strahlung_colorscale":    "YlGn",
        "bar_voll_color":          "#148f77",
        "bar_aktuell_color":       "#76d7c4",
        "precip_color":            "#1a5276",
        "temp_cold_threshold":     25,
        "temp_hot_threshold":      33,
        "temp_colors":             ["#f39c12", "#e74c3c", "#7b241c"],
    },
}

# Recommendation: Merge KOORDINATEN and KONTINENTE logic into the STAEDTE dict 
# to reduce maintenance overhead.

# ---------------------------------------------------------------------------
# Daten vorladen
# ---------------------------------------------------------------------------
print("Lade Daten...")
DATEN = {name: load_data(cfg["filename"]) for name, cfg in STAEDTE.items()}
print("Bereit.")

# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------
def theme_fig(fig, theme):
    t = THEMES[theme]
    fig.update_layout(
        plot_bgcolor=t["plot_bg"],
        paper_bgcolor=t["paper_bg"],
        font_color=t["font"],
        yaxis=dict(gridcolor=t["grid"], color=t["font"]),
        xaxis=dict(color=t["font"]),
        legend=dict(font=dict(color=t["font"]), bgcolor=t["paper_bg"]),
        title_font_color=t["font"],
    )
    return fig


def temp_farben(values, cold, hot, colors):
    c, m, h = colors
    return [c if v < cold else h if v > hot else m for v in values]


def linear_fit_fig(jahre, werte, bar_color, einheit, title, theme):
    t = THEMES[theme]
    mask = jahre < 2026
    x, y = jahre[mask], werte[mask]
    slope, intercept = np.polyfit(x, y, 1)
    trend_dekade = slope * 10
    fit_y = slope * x + intercept
    richtung = "▲" if trend_dekade > 0 else "▼"

    fig = go.Figure()
    if einheit == "°C":
        fig.add_trace(go.Scatter(
            x=x, y=y.round(2), mode="lines+markers", name="Jahresmittel",
            line=dict(color=bar_color, width=2), marker=dict(size=6),
            hovertemplate="%{x}: %{y:.2f} °C<extra></extra>"))
        label    = f"{trend_dekade:+.3f} °C/Dekade"
        ann_text = f"{richtung} <b>{abs(trend_dekade):.3f} °C pro Dekade</b>"
    else:
        fig.add_trace(go.Bar(
            x=x, y=y.round(1), name="Jahresniederschlag",
            marker_color=bar_color,
            hovertemplate="%{x}: %{y:.0f} mm<extra></extra>"))
        label    = f"{trend_dekade:+.1f} mm/Dekade"
        ann_text = f"{richtung} <b>{abs(trend_dekade):.1f} mm pro Dekade</b>"

    fig.add_trace(go.Scatter(
        x=x, y=fit_y.round(3), mode="lines",
        name=f"Linearer Trend ({label})",
        line=dict(color="#e74c3c", width=2, dash="dash")))
    fig.add_annotation(
        x=0.02, y=0.95, xref="paper", yref="paper", showarrow=False,
        text=ann_text, font=dict(size=14, color="#e74c3c"),
        bgcolor=t["ann_bg"], borderpad=8)
    fig.update_layout(
        title=title, xaxis_title="Jahr", yaxis_title=einheit,
        xaxis=dict(dtick=5), legend=dict(orientation="h", y=1.05))
    return theme_fig(fig, theme)


# ---------------------------------------------------------------------------
# App Layout
# ---------------------------------------------------------------------------
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Wetterdaten – Städtevergleich"

KONTINENTE = {
    "Europa":      ["Wien", "Rom", "Lissabon", "Oslo", "Dublin"],
    "Afrika":      ["Casablanca", "Lagos", "Nairobi", "Kapstadt"],
    "Asien":       ["Medina", "Mumbai", "Shanghai", "Tokyo", "Yakutsk", "Kuala Lumpur"],
    "Nordamerika": ["Las Vegas", "Los Angeles", "New York"],
    "Südamerika":  ["Santiago", "Rio"],
    "Ozeanien":    ["Canberra", "Wellington"],
}

KOORDINATEN = {
    "Wien":        (48.2082,  16.3738),
    "Casablanca":  (33.5731,  -7.5898),
    "Medina":      (24.5247,  39.5692),
    "Rom":         (41.9028,  12.4964),
    "Lissabon":    (38.7223,  -9.1393),
    "Santiago":    (-33.4489, -70.6693),
    "Los Angeles": (34.0522, -118.2437),
    "Las Vegas":   (36.1699, -115.1398),
    "New York":    (40.7128,  -74.0060),
    "Oslo":        (59.9139,   10.7522),
    "Tokyo":       (35.6762,  139.6503),
    "Shanghai":    (31.2304,  121.4737),
    "Mumbai":      (19.0760,   72.8777),
    "Dublin":      (53.3498,   -6.2603),
    "Canberra":    (-35.2809, 149.1300),
    "Wellington":  (-41.2866, 174.7756),
    "Yakutsk":     (62.0355,  129.6755),
    "Lagos":       (6.5244,     3.3792),
    "Nairobi":     (-1.2921,   36.8219),
    "Kapstadt":    (-33.9249,  18.4241),
    "Rio":         (-22.9068, -43.1729),
    "Kuala Lumpur": (3.1390,  101.6869),
}

kontinent_optionen = [{"label": k, "value": k} for k in KONTINENTE]
DEFAULT_KONTINENT = "Europa"
DEFAULT_STADT = sorted(KONTINENTE[DEFAULT_KONTINENT])[0]

app.layout = html.Div(
    id="main-container",
    style={"fontFamily": "Arial, sans-serif", "maxWidth": "1300px",
           "margin": "0 auto", "padding": "12px 20px", "minHeight": "100vh",
           "transition": "background-color 0.3s, color 0.3s"},
    children=[
        dcc.Store(id="theme-store", data="light"),

        # Single top row: controls left | map right
        html.Div(
            style={"display": "flex", "alignItems": "flex-start",
                   "gap": "16px", "marginBottom": "10px"},
            children=[
                # ── Left column ──────────────────────────────────────────
                html.Div(
                    id="stadt-auswahl-container",
                    style={"display": "flex", "flexDirection": "column", "gap": "6px"},
                    children=[
                        html.H2(id="titel", style={"margin": "0 0 4px 0", "fontSize": "20px"}),
                        # Row 1: Kontinent + Stadt side by side
                        html.Div(
                            style={"display": "flex", "gap": "10px", "alignItems": "flex-end"},
                            children=[
                                html.Div([
                                    html.Label("Kontinent:", id="kontinent-label",
                                               style={"fontWeight": "bold", "fontSize": "12px",
                                                      "display": "block", "marginBottom": "2px"}),
                                    dcc.Dropdown(id="kontinent-dropdown",
                                                 options=kontinent_optionen,
                                                 value=DEFAULT_KONTINENT,
                                                 clearable=False,
                                                 style={"width": "160px", "fontSize": "13px"}),
                                ]),
                                html.Div([
                                    html.Label("Stadt:", id="stadt-label",
                                               style={"fontWeight": "bold", "fontSize": "12px",
                                                      "display": "block", "marginBottom": "2px"}),
                                    dcc.Dropdown(id="stadt-dropdown",
                                                 value=DEFAULT_STADT,
                                                 clearable=False,
                                                 style={"width": "160px", "fontSize": "13px"}),
                                ]),
                            ]
                        ),
                        # Row 2: Ansicht + Jahr side by side
                        html.Div(
                            style={"display": "flex", "gap": "10px", "alignItems": "flex-end"},
                            children=[
                                html.Div([
                                    html.Label("Ansicht:", id="ansicht-label",
                                               style={"fontWeight": "bold", "fontSize": "12px",
                                                      "display": "block", "marginBottom": "2px"}),
                                    dcc.Dropdown(
                                        id="tabs",
                                        value="jahresverlauf",
                                        clearable=False,
                                        style={"width": "200px", "fontSize": "13px"},
                                        options=[
                                            {"label": "Strahlung nach Jahr",      "value": "jahresverlauf"},
                                            {"label": "Strahlung Zeitreihe",      "value": "zeitreihe"},
                                            {"label": "Strahlung Jahressummen",   "value": "jahressummen"},
                                            {"label": "Temperaturen",             "value": "temperaturen"},
                                            {"label": "Niederschlag",             "value": "niederschlag"},
                                            {"label": "Temp. Jahrestrend",        "value": "temp_trend"},
                                            {"label": "Niederschlag Jahrestrend", "value": "precip_trend"},
                                        ],
                                    ),
                                ]),
                                html.Div(id="jahr-selector-container", style={"display": "none"}, children=[
                                    html.Label("Jahr:", id="jahr-label",
                                               style={"fontWeight": "bold", "fontSize": "12px",
                                                      "display": "block", "marginBottom": "2px"}),
                                    dcc.Dropdown(id="jahr-dropdown", clearable=False,
                                                 style={"width": "140px", "fontSize": "13px"}),
                                ]),
                                html.Div(id="temp-selector-container", style={"display": "none"}, children=[
                                    html.Label("Jahr:", id="temp-label",
                                               style={"fontWeight": "bold", "fontSize": "12px",
                                                      "display": "block", "marginBottom": "2px"}),
                                    dcc.Dropdown(id="temp-dropdown", clearable=False,
                                                 style={"width": "140px", "fontSize": "13px"}),
                                ]),
                                html.Div(id="precip-selector-container", style={"display": "none"}, children=[
                                    html.Label("Jahr:", id="precip-label",
                                               style={"fontWeight": "bold", "fontSize": "12px",
                                                      "display": "block", "marginBottom": "2px"}),
                                    dcc.Dropdown(id="precip-dropdown", clearable=False,
                                                 style={"width": "140px", "fontSize": "13px"}),
                                ]),
                            ]
                        ),
                    ]
                ),

                # ── Right column: theme toggle + map ─────────────────────
                html.Div(
                    style={"flex": "1", "display": "flex", "flexDirection": "column",
                           "alignItems": "flex-end", "gap": "6px"},
                    children=[
                        html.Button(
                            id="theme-toggle",
                            n_clicks=0,
                            style={"padding": "5px 14px", "borderRadius": "16px",
                                   "border": "none", "cursor": "pointer",
                                   "fontSize": "12px", "fontWeight": "bold"},
                        ),
                        dcc.Graph(id="world-map", style={"width": "100%", "height": "180px"},
                                  config={"scrollZoom": False, "displayModeBar": False}),
                    ]
                ),
            ]
        ),

        html.Div(id="tab-inhalt", style={"marginTop": "8px"}),
    ]
)


# ---------------------------------------------------------------------------
# Theme-Callbacks
# ---------------------------------------------------------------------------
@app.callback(
    Output("theme-store", "data"),
    Input("theme-toggle", "n_clicks"),
    State("theme-store", "data"),
    prevent_initial_call=True,
)
def toggle_theme(_n, current):
    return "dark" if current == "light" else "light"


@app.callback(
    Output("main-container", "style"),
    Output("theme-toggle", "children"),
    Output("theme-toggle", "style"),
    Input("theme-store", "data"),
)
def update_container_style(theme):
    t = THEMES[theme]
    container_style = {
        "fontFamily": "Arial, sans-serif", "maxWidth": "1300px",
        "margin": "0 auto", "padding": "20px", "minHeight": "100vh",
        "backgroundColor": t["container_bg"], "color": t["font"],
    }
    btn_style = {
        "padding": "8px 18px", "borderRadius": "20px", "border": "none",
        "cursor": "pointer", "fontSize": "14px", "fontWeight": "bold",
        "backgroundColor": t["toggle_bg"], "color": t["toggle_fg"],
    }
    return container_style, t["toggle_label"], btn_style


@app.callback(
    Output("titel", "children"),
    Output("titel", "style"),
    Output("kontinent-label", "style"),
    Output("stadt-label", "style"),
    Output("ansicht-label", "style"),
    Output("kontinent-dropdown", "style"),
    Output("stadt-dropdown", "style"),
    Output("tabs", "style"),
    Input("stadt-dropdown", "value"),
    Input("theme-store", "data"),
)
def update_titel(stadt, theme):
    t = THEMES[theme]
    cfg = STAEDTE[stadt]
    farbe = cfg[f"h1_color_{theme}"]
    lbl = {"fontWeight": "bold", "fontSize": "12px", "display": "block",
           "marginBottom": "2px", "color": t["font"]}
    dd_city = {"width": "160px", "fontSize": "13px",
               "backgroundColor": t["plot_bg"], "color": t["font"]}
    dd_tab  = {"width": "200px", "fontSize": "13px",
               "backgroundColor": t["plot_bg"], "color": t["font"]}
    return (f"Wetterdaten {stadt}",
            {"margin": "0 0 4px 0", "fontSize": "20px", "color": farbe},
            lbl, lbl, lbl, dd_city, dd_city, dd_tab)


@app.callback(
    Output("stadt-dropdown", "options"),
    Output("stadt-dropdown", "value"),
    Input("kontinent-dropdown", "value"),
    State("stadt-dropdown", "value"),
)
def update_stadt_optionen(kontinent, aktuelle_stadt):
    staedte = sorted(KONTINENTE[kontinent])
    opts = [{"label": s, "value": s} for s in staedte]
    neuer_wert = aktuelle_stadt if aktuelle_stadt in staedte else staedte[0]
    return opts, neuer_wert


@app.callback(
    Output("world-map", "figure"),
    Input("stadt-dropdown", "value"),
    Input("theme-store", "data"),
)
def render_world_map(selected, theme):
    t = THEMES[theme]
    staedte = list(KOORDINATEN.keys())
    lats  = [KOORDINATEN[s][0] for s in staedte]
    lons  = [KOORDINATEN[s][1] for s in staedte]
    sizes = [18 if s == selected else 10 for s in staedte]
    colors = [STAEDTE[s]["bar_voll_color"] for s in staedte]
    borders = ["white" if s == selected else t["paper_bg"] for s in staedte]
    bwidths = [3 if s == selected else 1 for s in staedte]

    fig = go.Figure(go.Scattergeo(
        lat=lats, lon=lons,
        text=staedte,
        customdata=staedte,
        mode="markers+text",
        textposition="top center",
        textfont=dict(size=10, color=t["font"]),
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(color=borders, width=bwidths),
        ),
        hovertemplate="%{text}<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor=t["paper_bg"],
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(
            showland=True,
            landcolor="#d4d4d4" if theme == "light" else "#2e3347",
            showocean=True,
            oceancolor="#a8d0e8" if theme == "light" else "#1e2130",
            showcoastlines=True,
            coastlinecolor="#888888" if theme == "light" else "#555555",
            showcountries=True,
            countrycolor="#aaaaaa" if theme == "light" else "#444444",
            bgcolor=t["paper_bg"],
            projection_type="natural earth",
        ),
    )
    return fig


@app.callback(
    Output("kontinent-dropdown", "value"),
    Output("stadt-dropdown", "value", allow_duplicate=True),
    Input("world-map", "clickData"),
    prevent_initial_call=True,
)
def map_click(clickData):
    if not clickData:
        raise dash.exceptions.PreventUpdate
    stadt = clickData["points"][0]["text"]
    for kontinent, staedte in KONTINENTE.items():
        if stadt in staedte:
            return kontinent, stadt
    raise dash.exceptions.PreventUpdate


# ---------------------------------------------------------------------------
# Year-selector visibility, options, and styling
# ---------------------------------------------------------------------------
@app.callback(
    Output("jahr-selector-container", "style"),
    Output("temp-selector-container", "style"),
    Output("precip-selector-container", "style"),
    Output("jahr-label", "style"),
    Output("temp-label", "style"),
    Output("precip-label", "style"),
    Output("jahr-dropdown", "style"),
    Output("temp-dropdown", "style"),
    Output("precip-dropdown", "style"),
    Input("tabs", "value"),
    Input("theme-store", "data"),
)
def update_selector_visibility(tab, theme):
    t = THEMES[theme]
    label_style = {"fontWeight": "bold", "fontSize": "12px", "display": "block",
                   "marginBottom": "2px", "color": t["font"]}
    dd_style = {"width": "140px", "fontSize": "13px",
                "backgroundColor": t["plot_bg"], "color": t["font"]}

    def vis(show):
        return {"display": "block" if show else "none"}

    return (
        vis(tab == "jahresverlauf"),
        vis(tab == "temperaturen"),
        vis(tab == "niederschlag"),
        label_style, label_style, label_style,
        dd_style, dd_style, dd_style,
    )


@app.callback(
    Output("jahr-dropdown", "options"),
    Output("jahr-dropdown", "value"),
    Input("stadt-dropdown", "value"),
)
def update_jahr_options(stadt):
    alle_jahre = DATEN[stadt]["alle_jahre"]
    opts = [{"label": "Ø alle Jahre", "value": "alle"}] + [{"label": str(j), "value": j} for j in alle_jahre]
    return opts, "alle"


@app.callback(
    Output("temp-dropdown", "options"),
    Output("temp-dropdown", "value"),
    Input("stadt-dropdown", "value"),
)
def update_temp_options(stadt):
    alle_jahre = DATEN[stadt]["alle_jahre"]
    opts = [{"label": "Ø alle Jahre", "value": "alle"}] + [{"label": str(j), "value": j} for j in alle_jahre]
    return opts, "alle"


@app.callback(
    Output("precip-dropdown", "options"),
    Output("precip-dropdown", "value"),
    Input("stadt-dropdown", "value"),
)
def update_precip_options(stadt):
    alle_jahre = DATEN[stadt]["alle_jahre"]
    opts = [{"label": "Ø alle Jahre", "value": "alle"}] + [{"label": str(j), "value": j} for j in alle_jahre]
    return opts, "alle"


# ---------------------------------------------------------------------------
# Tab-Callback
# ---------------------------------------------------------------------------
@app.callback(
    Output("tab-inhalt", "children"),
    Input("tabs", "value"),
    Input("stadt-dropdown", "value"),
    Input("theme-store", "data"),
)
def render_tab(tab, stadt, theme):
    d   = DATEN[stadt]
    cfg = STAEDTE[stadt]
    t   = THEMES[theme]
    monthly          = d["monthly"]
    jaehrlich        = d["jaehrlich"]
    temp_jaehrlich   = d["temp_jaehrlich"]
    precip_jaehrlich = d["precip_jaehrlich"]

    jaehrlich_voll    = jaehrlich[jaehrlich["Jahr"] < 2026]
    jaehrlich_aktuell = jaehrlich[jaehrlich["Jahr"] == 2026]
    jaehrlich_mittel  = jaehrlich_voll["kWh_Jahr"].mean()

    if tab == "jahresverlauf":
        return dcc.Graph(id="jahres-graph", style={"height": "500px"})

    elif tab == "jahressummen":
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=jaehrlich_voll["Jahr"], y=jaehrlich_voll["kWh_Jahr"].round(0),
            name="Jahressumme", marker_color=cfg["bar_voll_color"],
            hovertemplate="%{x}: %{y:.0f} kWh/m²<extra></extra>",
            text=jaehrlich_voll["kWh_Jahr"].round(0).astype(int),
            textposition="outside", textfont=dict(size=9)))
        if not jaehrlich_aktuell.empty:
            fig.add_trace(go.Bar(
                x=jaehrlich_aktuell["Jahr"], y=jaehrlich_aktuell["kWh_Jahr"].round(0),
                name="2026 (unvollständig)", marker_color=cfg["bar_aktuell_color"],
                marker_pattern_shape="/",
                hovertemplate="%{x}: %{y:.0f} kWh/m² (bis März)<extra></extra>",
                text=jaehrlich_aktuell["kWh_Jahr"].round(0).astype(int),
                textposition="outside", textfont=dict(size=9)))
        fig.add_hline(y=jaehrlich_mittel, line_dash="dash", line_color="#e74c3c",
                      annotation_text=f"Ø {jaehrlich_mittel:.0f} kWh/m²",
                      annotation_position="top left",
                      annotation_font_color=t["font"])
        fig.update_layout(
            title=f"Gesamte Solarenergie pro Jahr – {stadt}",
            xaxis_title="Jahr", yaxis_title="kWh/m²",
            xaxis=dict(dtick=5, tickangle=-45),
            legend=dict(orientation="h", y=1.05), bargap=0.15)
        return dcc.Graph(figure=theme_fig(fig, theme), style={"height": "580px"})

    elif tab == "zeitreihe":
        fig = go.Figure(go.Bar(
            x=monthly["Datum"], y=monthly["kWh_Tag"].round(1),
            marker_color=cfg["bar_voll_color"],
            hovertemplate="%{x|%b %Y}: %{y} kWh/m²<extra></extra>"))
        fig.update_layout(
            title=f"Monatliche Solarenergie – {stadt}",
            xaxis_title="Datum", yaxis_title="kWh/m²",
            xaxis=dict(rangeslider=dict(visible=True,
                                        bgcolor=t["plot_bg"])))
        return dcc.Graph(figure=theme_fig(fig, theme), style={"height": "550px"})

    elif tab == "temperaturen":
        return dcc.Graph(id="temp-graph", style={"height": "500px"})

    elif tab == "niederschlag":
        return dcc.Graph(id="precip-graph", style={"height": "500px"})

    elif tab == "temp_trend":
        jahre = temp_jaehrlich["Jahr"].values
        werte = temp_jaehrlich["Temp_Jahr"].values
        fig = linear_fit_fig(jahre, werte, cfg["bar_voll_color"], "°C",
                             f"Jährliche Durchschnittstemperatur – {stadt}", theme)
        return dcc.Graph(figure=fig, style={"height": "520px"})

    elif tab == "precip_trend":
        jahre = precip_jaehrlich["Jahr"].values
        werte = precip_jaehrlich["Precip_Jahr"].values
        fig = linear_fit_fig(jahre, werte, cfg["precip_color"], "mm",
                             f"Jährlicher Gesamtniederschlag – {stadt}", theme)
        return dcc.Graph(figure=fig, style={"height": "520px"})


# ---------------------------------------------------------------------------
# Sub-Callbacks
# ---------------------------------------------------------------------------
@app.callback(
    Output("jahres-graph", "figure"),
    Input("jahr-dropdown", "value"),
    Input("stadt-dropdown", "value"),
    Input("theme-store", "data"),
)
def update_jahresgraph(jahr, stadt, theme):
    if jahr is None:
        return go.Figure()
    d = DATEN[stadt]
    cfg = STAEDTE[stadt]
    sc = cfg["strahlung_colorscale"]
    if jahr == "alle":
        x = d["monatsmittel"]["MonatName"]
        y = d["monatsmittel"]["kWh_Mittel"].round(1)
        titel = f"Ø Solarenergie pro Monat – {stadt}"
    else:
        gefiltert = d["monthly"][d["monthly"]["Jahr"] == jahr].copy()
        gefiltert["MonatName"] = gefiltert["Monat"].map(MONATSNAMEN)
        x = gefiltert["MonatName"]
        y = gefiltert["kWh_Tag"].round(1)
        titel = f"Solarenergie {jahr} – {stadt}, kWh/m² pro Monat"
    fig = go.Figure(go.Bar(
        x=x, y=y,
        marker_color=getattr(px.colors.sequential, sc),
        text=y, textposition="outside"))
    fig.update_layout(title=titel, xaxis_title="Monat", yaxis_title="kWh/m²")
    return theme_fig(fig, theme)


@app.callback(
    Output("temp-graph", "figure"),
    Input("temp-dropdown", "value"),
    Input("stadt-dropdown", "value"),
    Input("theme-store", "data"),
)
def update_tempgraph(auswahl, stadt, theme):
    d = DATEN[stadt]
    cfg = STAEDTE[stadt]
    t = THEMES[theme]
    if auswahl == "alle":
        x = d["temp_mittel"]["MonatName"]
        y = d["temp_mittel"]["Temp_Avg"].round(1)
        titel = f"Ø Monatstemperatur – {stadt}"
    else:
        df = d["temp_monatlich"][d["temp_monatlich"]["Jahr"] == auswahl].copy()
        df["MonatName"] = df["Monat"].map(MONATSNAMEN)
        x, y = df["MonatName"], df["Temp_Avg"].round(1)
        titel = f"Monatstemperatur {auswahl} – {stadt}"
    mittel = y.mean()
    farben = temp_farben(y, cfg["temp_cold_threshold"],
                         cfg["temp_hot_threshold"], cfg["temp_colors"])
    fig = go.Figure(go.Bar(x=x, y=y, marker_color=farben, text=y,
                           textposition="outside",
                           hovertemplate="%{x}: %{y:.1f} °C<extra></extra>"))
    if cfg["temp_cold_threshold"] <= 0:
        fig.add_hline(y=0, line_color=t["grid"], line_width=1)
    fig.add_hline(y=mittel, line_dash="dash", line_color="#8e44ad",
                  annotation_text=f"Ø {mittel:.1f} °C",
                  annotation_position="top left",
                  annotation_font_color=t["font"])
    fig.update_layout(title=titel, xaxis_title="Monat", yaxis_title="°C")
    return theme_fig(fig, theme)


@app.callback(
    Output("precip-graph", "figure"),
    Input("precip-dropdown", "value"),
    Input("stadt-dropdown", "value"),
    Input("theme-store", "data"),
)
def update_precipgraph(auswahl, stadt, theme):
    d = DATEN[stadt]
    cfg = STAEDTE[stadt]
    t = THEMES[theme]
    pm = d["precip_monatlich"]
    if auswahl == "alle":
        x = d["precip_mittel"]["MonatName"]
        y = d["precip_mittel"]["Niederschlag_Tag"].round(1)
        titel = f"Ø Monatsniederschlag – {stadt}"
        jahressumme = pm.groupby("Jahr")["Niederschlag_Tag"].sum().mean()
        ann = f"Ø Jahressumme: {jahressumme:.0f} mm"
    else:
        df = pm[pm["Jahr"] == auswahl].copy()
        df["MonatName"] = df["Monat"].map(MONATSNAMEN)
        x, y = df["MonatName"], df["Niederschlag_Tag"].round(1)
        titel = f"Monatsniederschlag {auswahl} – {stadt}"
        ann = f"Jahressumme: {y.sum():.0f} mm"
    fig = go.Figure(go.Bar(x=x, y=y, marker_color=cfg["precip_color"],
                           text=y, textposition="outside",
                           hovertemplate="%{x}: %{y:.1f} mm<extra></extra>"))
    fig.update_layout(
        title=titel, xaxis_title="Monat", yaxis_title="mm",
        annotations=[dict(x=0.01, y=0.97, xref="paper", yref="paper",
                          text=ann, showarrow=False,
                          font=dict(size=13, color=t["font"]),
                          bgcolor=t["ann_bg"], borderpad=6)])
    return theme_fig(fig, theme)


app.clientside_callback(
    """
    function(theme) {
        if (theme === 'dark') {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
        return theme;
    }
    """,
    Output("theme-store", "id"),   # dummy output – just triggers the JS
    Input("theme-store", "data"),
)

if __name__ == "__main__":
    webbrowser.open('http://localhost:8055')
    app.run(debug=True, port=8055)
