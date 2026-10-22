from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date, timedelta
from pathlib import Path

from build_instagram_continuity_2026_10 import ROOT, build_card


OUT = ROOT / "continuity-2026-10-25"

# Cada fila usa un hecho verificable de VARPAL y un arte distinto. No hay precios,
# fechas de entrega, direcciones ni nombres de proveedores externos.
TOPICS = [
    ("cobertura-envios/01-tu-ciudad-eeuu.jpg", "¿Tu caja sale de otro estado?", "Conéctala con Miami", "origen-usa", "VARPAL coordina envíos con origen en cualquiera de los 50 estados de EE. UU."),
    ("calcula-envio.jpg", "¿Qué datos necesita tu cotización?", "Peso, medidas y destino", "datos-cotizacion", "Comparte peso, medidas, contenido y ciudad de entrega para orientar tu cotización."),
    ("portal-cliente.jpg", "¿Tu paquete tiene número VP?", "Identifícalo antes de enviarlo", "numero-vp", "El número VP permite asociar cada paquete con la cuenta correcta."),
    ("paso-2-almacen.jpg", "¿Llegaron varias compras?", "Consulta la consolidación", "consolidacion", "La consolidación permite organizar varios paquetes antes de elegir el despacho."),
    ("paso-3-cotiza-aereo-maritimo.jpg", "¿Peso real o volumétrico?", "Mide la caja completa", "peso-facturable", "El peso facturable depende de las medidas y de la regla aplicable al envío."),
    ("paso-1-casillero.jpg", "¿Vas a enviar algo frágil?", "Protege cada espacio", "fragil", "Un empaque ajustado reduce el movimiento interno durante el manejo de la caja."),
    ("pickup.jpg", "¿Necesitas coordinar la recogida?", "Regístrate y confirma cobertura", "recogida", "Abre primero tu casillero; después VARPAL confirma cobertura, costo y horario de recogida."),
    ("rastreo-envios.jpg", "¿Ya tienes tu WR?", "Consulta el rastreo", "wr-rastreo", "Conserva tu número WR para consultar el estado disponible de tu envío."),
    ("aereo.jpg", "¿Cuándo conviene el aéreo?", "Revisa contenido y prioridad", "aereo", "La modalidad se orienta según el contenido, el peso, las medidas y el destino."),
    ("maritimo.jpg", "¿Tu carga ocupa más espacio?", "Consulta la vía marítima", "maritimo", "La vía marítima puede evaluarse según el volumen, el contenido y la ciudad de entrega."),
    ("cobertura-envios/04-venezuela-entrega.jpg", "¿A qué estado de Venezuela va?", "Indica la ciudad final", "destino-venezuela", "VARPAL coordina entregas en los 24 estados de Venezuela según la modalidad disponible."),
    ("casillero.jpg", "¿Comprarás en línea?", "Abre el casillero antes", "compras-online", "Usa tu número VP al dirigir las compras a la recepción de VARPAL en Miami."),
    ("pre-alerta.jpg", "¿La etiqueta se lee completa?", "Revísala antes de entregar", "etiqueta", "Mantén visible la identificación y confirma el contenido antes de cerrar la caja."),
    ("hero.jpg", "¿Buscas atención en español?", "Habla directo con VARPAL", "atencion", "VARPAL acompaña el proceso desde la recepción en Miami hasta la entrega coordinada en Venezuela."),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_assets() -> None:
    source_root = ROOT / "imagenes-pagina-web"
    for index, (source_name, headline, cta, slug, _fact) in enumerate(TOPICS, start=1):
        source = (source_root / source_name).resolve()
        if not source.exists():
            raise FileNotFoundError(source)
        build_card(source, OUT / f"{index:02d}-{slug}-feed.jpg", headline, cta, story=False)
        build_card(source, OUT / f"{index:02d}-{slug}-story.jpg", headline, cta, story=True)


def build_queue(commit: str, output: Path) -> None:
    if len(commit) < 40:
        raise ValueError("Se requiere el SHA completo del commit que contiene los assets")
    posts: list[dict] = []
    start = date(2026, 10, 25)
    hashtags = ["#VarpalCorp", "#EnviosAVenezuela", "#CasilleroMiami", "#VenezolanosEnUSA", "#MiamiVenezuela"]
    for index, (_source, headline, cta, slug, fact) in enumerate(TOPICS, start=1):
        day = start + timedelta(days=index - 1)
        for media_type, hour, suffix in (("image", "11:00", "feed"), ("story", "19:00", "story")):
            filename = f"{index:02d}-{slug}-{suffix}.jpg"
            post = {
                "key": f"continuity-2026-10-25-d{index:02d}-{suffix}-{slug}",
                "fecha_post": day.isoformat(),
                "hora_post": hour,
                "timezone": "America/New_York",
                "media_type": media_type,
                "filename": filename,
                "image_url": f"https://raw.githubusercontent.com/latinking26us-hub/varpal-images/{commit}/continuity-2026-10-25/{filename}",
                "asset_sha256": digest(OUT / filename),
                "asset_width": 1080,
                "asset_height": 1350 if media_type == "image" else 1920,
                "proposito": fact,
                "blockers": [],
                "approved": False,
            }
            if media_type == "image":
                post["caption"] = (
                    f"{headline}\n\n{fact}\n\n"
                    f"Siguiente paso: {cta.lower()}.\n\n"
                    "Escríbenos por WhatsApp 👉 +1 786 448 1426\n"
                    "Conoce el proceso 👉 varpalcorp.com"
                )
                post["hashtags"] = hashtags
                post["alt_text"] = f"Pieza informativa de VARPAL sobre {slug.replace('-', ' ')}."
            else:
                post["alt_text_interno"] = f"Story de VARPAL: {headline} {cta}."
            posts.append(post)
    output.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", help="SHA publicado para generar el JSON")
    parser.add_argument("--queue", type=Path, help="Ruta del JSON candidato")
    args = parser.parse_args()
    build_assets()
    if args.commit and args.queue:
        build_queue(args.commit, args.queue)
    print(f"assets={len(TOPICS) * 2} out={OUT}")


if __name__ == "__main__":
    main()
