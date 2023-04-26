import csv
import requests

# Obtener la lista de reproducción de Pluto TV
response = requests.get("https://gist.githubusercontent.com/mkudev/9cef0b6719d95d8fa827c203904711f7/raw/255c6a81bd391a5ef28f61fab894f8a50c0f533d/pluto.m3u")
raw_data = response.text

# Crear una lista de elementos de la lista de reproducción de Pluto TV
elements = []
for line in raw_data.splitlines():
    if line.startswith("#EXTINF"):
        element = {"title": None, "hls_url": None, "poster_url": None}
        element["title"] = line.split(",")[1]
        if "tvg-logo" in line:
            element["poster_url"] = line.split('tvg-logo="')[1].split('"')[0]
    elif line.startswith("http"):
        element["hls_url"] = line
        elements.append(element)

# Generar los shortcodes de reproductor de video y guardarlos en un archivo de texto
with open("pluto.txt", "w") as txtfile:
    for element in elements:
        shortcode = f'[bzplayer hls="{element["hls_url"]}" poster="{element["poster_url"]}" width="800" height="540" muted="false" selector="true"]\n'
        txtfile.write(shortcode)

# Guardar los detalles del canal en un archivo CSV, incluyendo el shortcode de reproductor de video
with open("pluto.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Título", "URL de transmisión", "URL del póster", "Shortcode"])
    for element in elements:
        shortcode = f'[bzplayer hls="{element["hls_url"]}" poster="{element["poster_url"]}" width="800" height="540" muted="false" selector="true"]'
        writer.writerow([element["title"], element["hls_url"], element["poster_url"], shortcode])

print("Archivos 'pluto.txt' y 'pluto.csv' generados correctamente.")
