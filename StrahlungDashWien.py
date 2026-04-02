from weather_dash_lib import create_app

app = create_app({
    "filename":                 "wien_wetter_vollständig_03_2026.csv",
    "title":                    "Wetterdaten Wien",
    "city":                     "Wien",
    "h1_color":                 "#2c3e50",
    "strahlung_colorscale":     "YlOrRd",
    "bar_voll_color":           "#e67e22",
    "bar_aktuell_color":        "#f39c12",
    "precip_color":             "#2980b9",
    "precip_annotation_color":  "#2c3e50",
    "precip_annotation_bg":     "#ecf0f1",
    "temp_cold_threshold":      0,
    "temp_hot_threshold":       20,
    "temp_colors":              ["#3498db", "#f39c12", "#e74c3c"],
    "port":                     8050,
})

if __name__ == "__main__":
    app.run(debug=True, port=8050)
