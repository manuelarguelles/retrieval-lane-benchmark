"""Assemble index.html (for embedding) and standalone.html (opens in a browser)."""
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PARTES = ["_head.html","_css2.html","_body1.html","_body2.html","_body3.html","_body4.html"]

datos = (AQUI/"data.json").read_text(encoding="utf-8")
html  = "\n".join((AQUI/p).read_text(encoding="utf-8") for p in PARTES)
js    = (AQUI/"_js.html").read_text(encoding="utf-8")

# The JSON is inlined: the viewer CSP blocks requests to any other host, so the
# page cannot go and fetch its own data file.
inline = "<script>window.__DATA__=" + datos.replace("</", "<\\/") + ";</script>\n"
cuerpo = html + "\n" + inline + js
(AQUI/"index.html").write_text(cuerpo, encoding="utf-8")

cabeza, resto = cuerpo.split("<header", 1)
(AQUI/"standalone.html").write_text(
    '<!doctype html><html lang="es"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
    + cabeza + "</head><body>\n<header" + resto + "\n</body></html>", encoding="utf-8")
print("index.html", (AQUI/"index.html").stat().st_size, "· standalone.html",
      (AQUI/"standalone.html").stat().st_size)
