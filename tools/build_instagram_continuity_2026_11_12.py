from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date, timedelta
from pathlib import Path

from build_instagram_continuity_2026_10 import ROOT, build_card


OUT = ROOT / "continuity-2026-11-12"

# Bloque de continuidad basado exclusivamente en imágenes operativas existentes de
# VARPAL. Cada pieza evita precios, fechas de entrega, direcciones y marcas de
# transportistas; las afirmaciones se limitan al flujo público ya verificado.
TOPICS = [
    (
        "casillero.jpg",
        "¿Compraste sin abrir casillero?",
        "Escríbeme CASILLERO por WhatsApp",
        "casillero-antes",
        "Abre tu casillero antes de dirigir compras a la recepción de VARPAL en Miami.",
        "CASILLERO",
    ),
    (
        "calcula-envio.jpg",
        "¿Cotizaste sin medir la caja?",
        "Escríbeme ENVÍO por WhatsApp",
        "datos-cotizacion",
        "Peso, medidas, contenido y ciudad de entrega permiten orientar mejor una cotización.",
        "ENVÍO",
    ),
    (
        "portal-cliente.jpg",
        "¿Tu paquete llegó sin número VP?",
        "Escríbeme ENVÍO por WhatsApp",
        "numero-vp",
        "El número VP ayuda a asociar el paquete con la cuenta correcta.",
        "ENVÍO",
    ),
    (
        "paso-2-almacen.jpg",
        "¿Tus compras quedaron separadas?",
        "Escríbeme ENVÍO por WhatsApp",
        "consolidacion",
        "Consulta la consolidación antes de elegir la modalidad de despacho.",
        "ENVÍO",
    ),
    (
        "paso-3-cotiza-aereo-maritimo.jpg",
        "¿Solo miraste el peso real?",
        "Escríbeme ENVÍO por WhatsApp",
        "peso-y-medidas",
        "El peso facturable puede depender del peso real, las medidas y la regla aplicable.",
        "ENVÍO",
    ),
    (
        "paso-1-casillero.jpg",
        "¿Algo frágil quedó suelto?",
        "Escríbeme ENVÍO por WhatsApp",
        "empaque-fragil",
        "Un empaque ajustado ayuda a reducir el movimiento interno durante el manejo.",
        "ENVÍO",
    ),
    (
        "pickup.jpg",
        "¿Pediste recogida sin registro?",
        "Escríbeme CASILLERO por WhatsApp",
        "recogida-confirmada",
        "Abre primero tu casillero; después se confirman cobertura, costo y horario de recogida.",
        "CASILLERO",
    ),
    (
        "rastreo-envios.jpg",
        "¿Perdiste de vista tu envío?",
        "Escríbeme ENVÍO por WhatsApp",
        "rastreo-wr",
        "Conserva tu número WR para consultar el estado disponible del envío.",
        "ENVÍO",
    ),
    (
        "aereo.jpg",
        "¿Elegiste modalidad sin revisar?",
        "Escríbeme ENVÍO por WhatsApp",
        "modalidad-aerea",
        "La orientación depende del contenido, el peso, las medidas y el destino.",
        "ENVÍO",
    ),
    (
        "maritimo.jpg",
        "¿Tu carga ocupa demasiado?",
        "Escríbeme ENVÍO por WhatsApp",
        "modalidad-maritima",
        "La vía marítima puede evaluarse según el volumen, el contenido y la ciudad de entrega.",
        "ENVÍO",
    ),
    (
        "cobertura-envios/04-venezuela-entrega.jpg",
        "¿Falta la ciudad de entrega?",
        "Escríbeme ENVÍO por WhatsApp",
        "destino-venezuela",
        "Indica la ciudad final para revisar la modalidad de entrega disponible en Venezuela.",
        "ENVÍO",
    ),
    (
        "personal-shopper.jpg",
        "¿Compraste sin tu número VP?",
        "Escríbeme CASILLERO por WhatsApp",
        "compras-online",
        "Usa tu número VP al dirigir compras en línea a la recepción de VARPAL.",
        "CASILLERO",
    ),
    (
        "pre-alerta.jpg",
        "¿La etiqueta quedó tapada?",
        "Escríbeme ENVÍO por WhatsApp",
        "etiqueta-visible",
        "Mantén visible la identificación y confirma el contenido antes de cerrar la caja.",
        "ENVÍO",
    ),
    (
        "hero.jpg",
        "¿Te falta una respuesta clara?",
        "Escríbeme ENVÍO por WhatsApp",
        "atencion-directa",
        "VARPAL orienta el proceso desde la recepción en Miami hasta la entrega coordinada en Venezuela.",
        "ENVÍO",
    ),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_assets() -> None:
    source_root = ROOT / "imagenes-pagina-web"
    for index, (source_name, headline, cta, slug, _fact, _keyword) in enumerate(TOPICS, start=1):
        source = (source_root / source_name).resolve()
        if not source.exists():
            raise FileNotFoundError(source)
        build_card(source, OUT / f"{index:02d}-{slug}-feed.jpg", headline, cta, story=False)
        build_card(source, OUT / f"{index:02d}-{slug}-story.jpg", headline, cta, story=True)


def build_queue(commit: str, output: Path) -> None:
    if len(commit) < 40:
        raise ValueError("Se requiere el SHA completo del commit que contiene los assets")
    posts: list[dict] = []
    start = date(2026, 11, 12)
    hashtags = [
        "#VarpalCorp",
        "#EnviosAVenezuela",
        "#CourierMiami",
        "#CasilleroMiami",
        "#VenezolanosEnUSA",
        "#MiamiVenezuela",
    ]
    for index, (_source, headline, cta, slug, fact, keyword) in enumerate(TOPICS, start=1):
        day = start + timedelta(days=index - 1)
        for media_type, hour, suffix in (("image", "11:00", "feed"), ("story", "19:00", "story")):
            filename = f"{index:02d}-{slug}-{suffix}.jpg"
            post = {
                "key": f"continuity-2026-11-12-d{index:02d}-{suffix}-{slug}",
                "fecha_post": day.isoformat(),
                "hora_post": hour,
                "timezone": "America/New_York",
                "media_type": media_type,
                "filename": filename,
                "image_url": (
                    "https://raw.githubusercontent.com/latinking26us-hub/varpal-images/"
                    f"{commit}/continuity-2026-11-12/{filename}"
                ),
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
                    f"Evita corregirlo después: confirma los datos antes de preparar tu {keyword.lower()}.\n\n"
                    f"escríbeme {keyword} por WhatsApp"
                )
                post["hashtags"] = hashtags
                post["alt_text"] = f"Pieza informativa de VARPAL sobre {slug.replace('-', ' ')}."
            else:
                post["alt_text_interno"] = f"Story de VARPAL: {headline} {fact} {cta}."
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
