from weather_dash_lib import create_app

app = create_app({
    "filename":                 "medina_wetter_vollständig_03_2026.csv",
    "title":                    "Wetterdaten Medina",
    "city":                     "Medina",
    "h1_color":                 "#6e2f00",
    "strahlung_colorscale":     "Oranges",
    "bar_voll_color":           "#c0392b",
    "bar_aktuell_color":        "#e59866",
    "precip_color":             "#6e2f00",
    "precip_annotation_color":  "#6e2f00",
    "precip_annotation_bg":     "#fdf2e9",
    "temp_cold_threshold":      25,
    "temp_hot_threshold":       35,
    "temp_colors":              ["#f39c12", "#c0392b", "#7b241c"],
    "port":                     8052,
})

if __name__ == "__main__":
    app.run(debug=True, port=8052)
