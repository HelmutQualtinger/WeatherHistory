import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, State

from weather_dash_lib import load_data, MONATSNAMEN

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
        "filename":                "wien_wetter_vollständig_03_2026.csv",
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
    "Casablanca": {
        "filename":                "casablanca_wetter_vollständig_03_2026.csv",
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
        "filename":                "medina_wetter_vollständig_03_2026.csv",
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
        "filename":                "rome_wetter_vollständig_03_2026.csv",
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
        "filename":                "lisbon_wetter_vollständig_03_2026.csv",
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
        "filename":                "santiago_wetter_vollständig_03_2026.csv",
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
    "Los Angeles": {
        "filename":                "losangeles_wetter_vollständig_03_2026.csv",
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
    "Oslo": {
        "filename":                "oslo_wetter_vollständig_03_2026.csv",
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
}

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

stadt_optionen = [{"label": s, "value": s} for s in STAEDTE]

app.layout = html.Div(
    id="main-container",
    style={"fontFamily": "Arial, sans-serif", "maxWidth": "1300px",
           "margin": "0 auto", "padding": "20px", "minHeight": "100vh"},
    children=[
        dcc.Store(id="theme-store", data="light"),

        # Header
        html.Div(
            style={"display": "flex", "justifyContent": "space-between",
                   "alignItems": "center", "marginBottom": "10px"},
            children=[
                html.H1(id="titel", style={"margin": 0}),
                html.Button(
                    id="theme-toggle",
                    n_clicks=0,
                    style={"padding": "8px 18px", "borderRadius": "20px",
                           "border": "none", "cursor": "pointer",
                           "fontSize": "14px", "fontWeight": "bold"},
                ),
            ]
        ),

        # Stadt-Auswahl
        html.Div(
            style={"display": "flex", "alignItems": "center",
                   "gap": "12px", "marginBottom": "16px"},
            children=[
                html.Label("Stadt:", id="stadt-label",
                            style={"fontWeight": "bold", "fontSize": "16px"}),
                dcc.Dropdown(
                    id="stadt-dropdown",
                    options=stadt_optionen,
                    value="Wien",
                    clearable=False,
                    style={"width": "220px", "fontSize": "15px"},
                ),
            ]
        ),

        dcc.Tabs(id="tabs", value="mittelwert", children=[
            dcc.Tab(label="Strahlung Monatsmittel",   value="mittelwert"),
            dcc.Tab(label="Strahlung nach Jahr",      value="jahresverlauf"),
            dcc.Tab(label="Strahlung Zeitreihe",      value="zeitreihe"),
            dcc.Tab(label="Strahlung Jahressummen",   value="jahressummen"),
            dcc.Tab(label="Temperaturen",             value="temperaturen"),
            dcc.Tab(label="Niederschlag",             value="niederschlag"),
            dcc.Tab(label="Temp. Jahrestrend",        value="temp_trend"),
            dcc.Tab(label="Niederschlag Jahrestrend", value="precip_trend"),
        ]),

        html.Div(id="tab-inhalt", style={"marginTop": "20px"}),
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
def toggle_theme(n, current):
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
    Output("stadt-label", "style"),
    Input("stadt-dropdown", "value"),
    Input("theme-store", "data"),
)
def update_titel(stadt, theme):
    t = THEMES[theme]
    cfg = STAEDTE[stadt]
    farbe = cfg[f"h1_color_{theme}"]
    return (f"Wetterdaten {stadt}",
            {"margin": 0, "color": farbe},
            {"fontWeight": "bold", "fontSize": "16px", "color": t["font"]})


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
    sc  = cfg["strahlung_colorscale"]

    monthly          = d["monthly"]
    jaehrlich        = d["jaehrlich"]
    monatsmittel     = d["monatsmittel"]
    temp_monatlich   = d["temp_monatlich"]
    temp_mittel      = d["temp_mittel"]
    precip_monatlich = d["precip_monatlich"]
    precip_mittel    = d["precip_mittel"]
    temp_jaehrlich   = d["temp_jaehrlich"]
    precip_jaehrlich = d["precip_jaehrlich"]
    alle_jahre       = d["alle_jahre"]

    jaehrlich_voll    = jaehrlich[jaehrlich["Jahr"] < 2026]
    jaehrlich_aktuell = jaehrlich[jaehrlich["Jahr"] == 2026]
    jaehrlich_mittel  = jaehrlich_voll["kWh_Jahr"].mean()

    dropdown_style = {
        "width": "200px",
        "backgroundColor": t["plot_bg"],
        "color": t["font"],
    }
    jahr_optionen = ([{"label": "Ø alle Jahre", "value": "alle"}]
                     + [{"label": str(j), "value": j} for j in alle_jahre])

    if tab == "mittelwert":
        fig = go.Figure(go.Bar(
            x=monatsmittel["MonatName"], y=monatsmittel["kWh_Mittel"].round(1),
            marker_color=getattr(px.colors.sequential, sc),
            text=monatsmittel["kWh_Mittel"].round(1), textposition="outside"))
        fig.update_layout(title=f"Ø Solarenergie pro Monat – {stadt}",
                          xaxis_title="Monat", yaxis_title="kWh/m²")
        return dcc.Graph(figure=theme_fig(fig, theme), style={"height": "500px"})

    elif tab == "jahresverlauf":
        return html.Div([
            html.Label("Jahr auswählen:",
                       style={"fontWeight": "bold", "color": t["font"]}),
            dcc.Dropdown(id="jahr-dropdown",
                         options=[{"label": str(j), "value": j} for j in alle_jahre],
                         value=alle_jahre[-1], clearable=False, style=dropdown_style),
            dcc.Graph(id="jahres-graph", style={"height": "500px"}),
        ])

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
        return html.Div([
            html.Label("Jahr auswählen:",
                       style={"fontWeight": "bold", "color": t["font"]}),
            dcc.Dropdown(id="temp-dropdown", options=jahr_optionen,
                         value="alle", clearable=False, style=dropdown_style),
            dcc.Graph(id="temp-graph", style={"height": "500px"}),
        ])

    elif tab == "niederschlag":
        return html.Div([
            html.Label("Jahr auswählen:",
                       style={"fontWeight": "bold", "color": t["font"]}),
            dcc.Dropdown(id="precip-dropdown", options=jahr_optionen,
                         value="alle", clearable=False, style=dropdown_style),
            dcc.Graph(id="precip-graph", style={"height": "500px"}),
        ])

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
    gefiltert = d["monthly"][d["monthly"]["Jahr"] == jahr].copy()
    gefiltert["MonatName"] = gefiltert["Monat"].map(MONATSNAMEN)
    fig = go.Figure(go.Bar(
        x=gefiltert["MonatName"], y=gefiltert["kWh_Tag"].round(1),
        marker_color=getattr(px.colors.sequential, sc),
        text=gefiltert["kWh_Tag"].round(1), textposition="outside"))
    fig.update_layout(title=f"Solarenergie {jahr} – {stadt}, kWh/m² pro Monat",
                      xaxis_title="Monat", yaxis_title="kWh/m²")
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
    app.run(debug=True, port=8055)
