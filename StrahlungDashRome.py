from weather_dash_lib import create_app

app = create_app({
    "filename":                 "rome_wetter_vollständig_03_2026.csv",
    "title":                    "Wetterdaten Rom",
    "city":                     "Rom",
    "h1_color":                 "#7b241c",
    "strahlung_colorscale":     "Reds",
    "bar_voll_color":           "#c0392b",
    "bar_aktuell_color":        "#e59866",
    "precip_color":             "#7b241c",
    "precip_annotation_color":  "#7b241c",
    "precip_annotation_bg":     "#fdedec",
    "temp_cold_threshold":      5,
    "temp_hot_threshold":       25,
    "temp_colors":              ["#3498db", "#f39c12", "#e74c3c"],
    "port":                     8053,
})

if __name__ == "__main__":
    app.run(debug=True, port=8053)
