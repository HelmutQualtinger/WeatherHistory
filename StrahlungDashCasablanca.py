from weather_dash_lib import create_app

app = create_app({
    "filename":                 "casablanca_wetter_vollständig_03_2026.csv",
    "title":                    "Wetterdaten Casablanca",
    "city":                     "Casablanca",
    "h1_color":                 "#1a5276",
    "strahlung_colorscale":     "solar",
    "bar_voll_color":           "#2980b9",
    "bar_aktuell_color":        "#85c1e9",
    "precip_color":             "#1a5276",
    "precip_annotation_color":  "#1a5276",
    "precip_annotation_bg":     "#eaf2ff",
    "temp_cold_threshold":      15,
    "temp_hot_threshold":       28,
    "temp_colors":              ["#3498db", "#f39c12", "#e74c3c"],
    "port":                     8051,
})

if __name__ == "__main__":
    app.run(debug=True, port=8051)
