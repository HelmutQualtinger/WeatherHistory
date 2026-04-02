import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px

MONATSNAMEN = {
    1: "Jän", 2: "Feb", 3: "Mär", 4: "Apr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Dez"
}


def load_data(filename):
    df = pd.read_csv(filename, parse_dates=["Datum"])
    df["Jahr"] = df["Datum"].dt.year
    df["Monat"] = df["Datum"].dt.month
    df["YearMonth"] = df["Datum"].dt.to_period("M")
    df["kWh_Tag"] = df["Strahlung_Avg"] * 24 / 1000
    df["Niederschlag_Tag"] = df["Niederschlag_Avg"] * 24

    monthly = df.groupby("YearMonth")["kWh_Tag"].sum().reset_index()
    monthly["Datum"] = monthly["YearMonth"].dt.to_timestamp()
    monthly["Jahr"] = monthly["Datum"].dt.year
    monthly["Monat"] = monthly["Datum"].dt.month

    jaehrlich = (df.groupby("Jahr")["kWh_Tag"].sum().reset_index()
                 .rename(columns={"kWh_Tag": "kWh_Jahr"}))

    monatsmittel = (monthly.groupby("Monat")["kWh_Tag"].mean().reset_index()
                    .rename(columns={"kWh_Tag": "kWh_Mittel"}))
    monatsmittel["MonatName"] = monatsmittel["Monat"].map(MONATSNAMEN)

    temp_monatlich = df.groupby(["Jahr", "Monat"])["Temp_Avg"].mean().reset_index()
    temp_mittel = temp_monatlich.groupby("Monat")["Temp_Avg"].mean().reset_index()
    temp_mittel["MonatName"] = temp_mittel["Monat"].map(MONATSNAMEN)

    precip_monatlich = df.groupby(["Jahr", "Monat"])["Niederschlag_Tag"].sum().reset_index()
    precip_mittel = precip_monatlich.groupby("Monat")["Niederschlag_Tag"].mean().reset_index()
    precip_mittel["MonatName"] = precip_mittel["Monat"].map(MONATSNAMEN)

    return dict(
        df=df,
        monthly=monthly,
        jaehrlich=jaehrlich,
        monatsmittel=monatsmittel,
        temp_monatlich=temp_monatlich,
        temp_mittel=temp_mittel,
        precip_monatlich=precip_monatlich,
        precip_mittel=precip_mittel,
        alle_jahre=sorted(df["Jahr"].unique()),
    )


def _temp_colors(values, cold_threshold, hot_threshold, colors):
    cold_c, mid_c, hot_c = colors
    return [cold_c if v < cold_threshold else hot_c if v > hot_threshold else mid_c for v in values]


def create_app(cfg):
    """
    cfg keys:
        filename, title, city, h1_color,
        strahlung_colorscale,           # e.g. "YlOrRd"
        bar_voll_color, bar_aktuell_color,
        precip_color, precip_annotation_color, precip_annotation_bg,
        temp_cold_threshold, temp_hot_threshold,
        temp_colors,                    # [cold_color, mid_color, hot_color]
        port
    """
    data = load_data(cfg["filename"])
    monthly = data["monthly"]
    jaehrlich = data["jaehrlich"]
    monatsmittel = data["monatsmittel"]
    temp_monatlich = data["temp_monatlich"]
    temp_mittel = data["temp_mittel"]
    precip_monatlich = data["precip_monatlich"]
    precip_mittel = data["precip_mittel"]
    alle_jahre = data["alle_jahre"]

    jaehrlich_voll = jaehrlich[jaehrlich["Jahr"] < 2026]
    jaehrlich_aktuell = jaehrlich[jaehrlich["Jahr"] == 2026]
    jaehrlich_mittel = jaehrlich_voll["kWh_Jahr"].mean()

    city = cfg["city"]
    sc = cfg["strahlung_colorscale"]
    jahr_optionen = ([{"label": "Ø alle Jahre", "value": "alle"}]
                     + [{"label": str(j), "value": j} for j in alle_jahre])

    app = dash.Dash(__name__, suppress_callback_exceptions=True)
    app.title = cfg["title"]

    app.layout = html.Div(
        style={"fontFamily": "Arial, sans-serif", "maxWidth": "1200px",
               "margin": "0 auto", "padding": "20px"},
        children=[
            html.H1(cfg["title"], style={"textAlign": "center", "color": cfg["h1_color"]}),
            dcc.Tabs(id="tabs", value="mittelwert", children=[
                dcc.Tab(label="Strahlung Monatsmittel",  value="mittelwert"),
                dcc.Tab(label="Strahlung nach Jahr",     value="jahresverlauf"),
                dcc.Tab(label="Strahlung Zeitreihe",     value="zeitreihe"),
                dcc.Tab(label="Strahlung Jahressummen",  value="jahressummen"),
                dcc.Tab(label="Temperaturen",            value="temperaturen"),
                dcc.Tab(label="Niederschlag",            value="niederschlag"),
            ]),
            html.Div(id="tab-inhalt", style={"marginTop": "20px"}),
        ]
    )

    # ------------------------------------------------------------------ #
    @app.callback(Output("tab-inhalt", "children"), Input("tabs", "value"))
    def render_tab(tab):
        if tab == "mittelwert":
            fig = go.Figure(go.Bar(
                x=monatsmittel["MonatName"], y=monatsmittel["kWh_Mittel"].round(1),
                marker_color=getattr(px.colors.sequential, sc),
                text=monatsmittel["kWh_Mittel"].round(1), textposition="outside",
            ))
            fig.update_layout(
                title=f"Ø Solarenergie pro Monat – {city} (2000–2026)",
                xaxis_title="Monat", yaxis_title="kWh/m²",
                plot_bgcolor="white", yaxis=dict(gridcolor="#eeeeee"))
            return dcc.Graph(figure=fig, style={"height": "500px"})

        elif tab == "jahresverlauf":
            return html.Div([
                html.Label("Jahr auswählen:", style={"fontWeight": "bold"}),
                dcc.Dropdown(id="jahr-dropdown",
                             options=[{"label": str(j), "value": j} for j in alle_jahre],
                             value=alle_jahre[-1], clearable=False, style={"width": "200px"}),
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
            fig.add_hline(y=jaehrlich_mittel, line_dash="dash", line_color="#c0392b",
                          annotation_text=f"Ø {jaehrlich_mittel:.0f} kWh/m²",
                          annotation_position="top left")
            fig.update_layout(
                title=f"Gesamte Solarenergie pro Jahr – {city} (2000–2026)",
                xaxis_title="Jahr", yaxis_title="kWh/m²", plot_bgcolor="white",
                yaxis=dict(gridcolor="#eeeeee"), xaxis=dict(dtick=1, tickangle=-45),
                legend=dict(orientation="h", y=1.05), bargap=0.15)
            return dcc.Graph(figure=fig, style={"height": "580px"})

        elif tab == "zeitreihe":
            fig = go.Figure(go.Bar(
                x=monthly["Datum"], y=monthly["kWh_Tag"].round(1),
                marker_color=cfg["bar_voll_color"],
                hovertemplate="%{x|%b %Y}: %{y} kWh/m²<extra></extra>"))
            fig.update_layout(
                title=f"Monatliche Solarenergie – {city}, alle Jahre",
                xaxis_title="Datum", yaxis_title="kWh/m²", plot_bgcolor="white",
                yaxis=dict(gridcolor="#eeeeee"), xaxis=dict(rangeslider=dict(visible=True)))
            return dcc.Graph(figure=fig, style={"height": "550px"})

        elif tab == "temperaturen":
            return html.Div([
                html.Label("Jahr auswählen:", style={"fontWeight": "bold"}),
                dcc.Dropdown(id="temp-dropdown", options=jahr_optionen,
                             value="alle", clearable=False, style={"width": "200px"}),
                dcc.Graph(id="temp-graph", style={"height": "500px"}),
            ])

        elif tab == "niederschlag":
            return html.Div([
                html.Label("Jahr auswählen:", style={"fontWeight": "bold"}),
                dcc.Dropdown(id="precip-dropdown", options=jahr_optionen,
                             value="alle", clearable=False, style={"width": "200px"}),
                dcc.Graph(id="precip-graph", style={"height": "500px"}),
            ])

    # ------------------------------------------------------------------ #
    @app.callback(Output("jahres-graph", "figure"), Input("jahr-dropdown", "value"))
    def update_jahresgraph(jahr):
        if jahr is None:
            return go.Figure()
        gefiltert = monthly[monthly["Jahr"] == jahr].copy()
        gefiltert["MonatName"] = gefiltert["Monat"].map(MONATSNAMEN)
        fig = go.Figure(go.Bar(
            x=gefiltert["MonatName"], y=gefiltert["kWh_Tag"].round(1),
            marker_color=getattr(px.colors.sequential, sc),
            text=gefiltert["kWh_Tag"].round(1), textposition="outside"))
        fig.update_layout(
            title=f"Solarenergie {jahr} – {city}, kWh/m² pro Monat",
            xaxis_title="Monat", yaxis_title="kWh/m²",
            plot_bgcolor="white", yaxis=dict(gridcolor="#eeeeee"))
        return fig

    # ------------------------------------------------------------------ #
    @app.callback(Output("temp-graph", "figure"), Input("temp-dropdown", "value"))
    def update_tempgraph(auswahl):
        if auswahl == "alle":
            x = temp_mittel["MonatName"]
            y = temp_mittel["Temp_Avg"].round(1)
            titel = f"Ø Monatstemperatur – {city} (2000–2025)"
        else:
            d = temp_monatlich[temp_monatlich["Jahr"] == auswahl].copy()
            d["MonatName"] = d["Monat"].map(MONATSNAMEN)
            x, y = d["MonatName"], d["Temp_Avg"].round(1)
            titel = f"Monatstemperatur {auswahl} – {city}"

        mittel = y.mean()
        farben = _temp_colors(y, cfg["temp_cold_threshold"], cfg["temp_hot_threshold"],
                              cfg["temp_colors"])
        fig = go.Figure(go.Bar(x=x, y=y, marker_color=farben,
                               text=y, textposition="outside",
                               hovertemplate="%{x}: %{y:.1f} °C<extra></extra>"))
        if cfg["temp_cold_threshold"] <= 0:
            fig.add_hline(y=0, line_color="#aaaaaa", line_width=1)
        fig.add_hline(y=mittel, line_dash="dash", line_color="#8e44ad",
                      annotation_text=f"Ø {mittel:.1f} °C", annotation_position="top left")
        fig.update_layout(title=titel, xaxis_title="Monat", yaxis_title="°C",
                          plot_bgcolor="white", yaxis=dict(gridcolor="#eeeeee"))
        return fig

    # ------------------------------------------------------------------ #
    @app.callback(Output("precip-graph", "figure"), Input("precip-dropdown", "value"))
    def update_precipgraph(auswahl):
        if auswahl == "alle":
            x = precip_mittel["MonatName"]
            y = precip_mittel["Niederschlag_Tag"].round(1)
            titel = f"Ø Monatsniederschlag – {city} (2000–2025)"
            jahressumme = precip_monatlich.groupby("Jahr")["Niederschlag_Tag"].sum().mean()
            annotation_text = f"Ø Jahressumme: {jahressumme:.0f} mm"
        else:
            d = precip_monatlich[precip_monatlich["Jahr"] == auswahl].copy()
            d["MonatName"] = d["Monat"].map(MONATSNAMEN)
            x, y = d["MonatName"], d["Niederschlag_Tag"].round(1)
            titel = f"Monatsniederschlag {auswahl} – {city}"
            annotation_text = f"Jahressumme: {y.sum():.0f} mm"

        fig = go.Figure(go.Bar(x=x, y=y, marker_color=cfg["precip_color"],
                               text=y, textposition="outside",
                               hovertemplate="%{x}: %{y:.1f} mm<extra></extra>"))
        fig.update_layout(
            title=titel, xaxis_title="Monat", yaxis_title="mm",
            plot_bgcolor="white", yaxis=dict(gridcolor="#eeeeee"),
            annotations=[dict(x=0.01, y=0.97, xref="paper", yref="paper",
                              text=annotation_text, showarrow=False,
                              font=dict(size=13, color=cfg["precip_annotation_color"]),
                              bgcolor=cfg["precip_annotation_bg"], borderpad=6)])
        return fig

    return app
