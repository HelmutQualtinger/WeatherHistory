from weather_dash_lib import create_app

app = create_app({
    "filename":                 "lisbon_wetter_vollständig_03_2026.csv",
    "title":                    "Wetterdaten Lissabon",
    "city":                     "Lissabon",
    "h1_color":                 "#1a6b8a",
    "strahlung_colorscale":     "Blues",
    "bar_voll_color":           "#2471a3",
    "bar_aktuell_color":        "#7fb3d3",
    "precip_color":             "#1a6b8a",
    "precip_annotation_color":  "#1a6b8a",
    "precip_annotation_bg":     "#eaf4fb",
    "temp_cold_threshold":      10,
    "temp_hot_threshold":       25,
    "temp_colors":              ["#3498db", "#f39c12", "#e74c3c"],
    "port":                     8054,
})

if __name__ == "__main__":
    app.run(debug=True, port=8054)
