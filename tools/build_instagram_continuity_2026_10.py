from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date, timedelta
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "continuity-2026-10-11"
LOGO = Path(r"C:\VARPAL\varpal-platform\services\api\app\static\varpal-logo.png")
if not LOGO.exists():
    LOGO = Path(r"C:\VARPAL\worktrees\codex-atoms-higgsfield-20260927\services\api\app\static\varpal-logo.png")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_REGULAR = Path(r"C:\Windows\Fonts\arial.ttf")


TOPICS = [
    ("casillero.jpg", "¿Vas a comprar esta semana?", "Abre tu casillero primero", "casillero", "Organiza tus compras con una dirección de recepción en Miami."),
    ("cobertura-envios/01-tu-ciudad-eeuu.jpg", "¿Envías desde otra ciudad?", "Consulta tu ruta a Miami", "cobertura", "Consulta cómo hacer llegar tu caja al punto de recepción en Miami."),
    ("paso-2-almacen.jpg", "¿Compras para tu negocio?", "Ordena tu consolidación", "consolidacion", "Agrupa tus compras antes de elegir la modalidad de envío."),
    ("calcula-envio.jpg", "¿El tamaño cambia tu cotización?", "Mide largo, ancho y alto", "medidas", "Las medidas y el peso ayudan a preparar una cotización útil."),
    ("rastreo-envios.jpg", "¿Quieres saber dónde va?", "Rastrea con tu número", "rastreo", "Conserva tu número de rastreo y consulta el estado en línea."),
    ("aereo.jpg", "¿Aéreo o marítimo?", "Consulta la opción adecuada", "modalidad", "La modalidad depende del tipo de envío, sus medidas y el destino."),
    ("paso-3-cotiza-aereo-maritimo.jpg", "¿Qué vas a enviar?", "Pregunta antes de empacar", "contenido", "Confirma las condiciones aplicables al contenido antes de preparar la caja."),
    ("../archivo-varpal-historia-clientes/final/varpal-clientes-reales-clean-1080.png", "¿Varias cajas para tu familia?", "Coordina antes de enviarlas", "familia", "Planifica el envío con tiempo y confirma la ciudad de entrega."),
    ("portal-cliente.jpg", "¿Tu compra ya llegó?", "Identifica cada paquete", "identificacion", "Incluye tu número VP para que el paquete pueda asociarse a tu cuenta."),
    ("paso-1-casillero.jpg", "¿Necesitas proteger lo frágil?", "Refuerza el empaque", "empaque", "Evita espacios sueltos y consulta si el contenido requiere protección adicional."),
    ("cobertura-envios/04-venezuela-entrega.jpg", "¿Enviar a otra ciudad?", "Confirma la entrega", "destino", "Indica la ciudad de destino para revisar la modalidad disponible."),
    ("pre-alerta.jpg", "¿Tu caja está lista?", "Revisa etiqueta y contenido", "revision", "Verifica que la identificación sea visible y que el empaque esté cerrado."),
    ("personal-shopper.jpg", "¿Planeas compras en EE. UU.?", "Usa tu casillero VARPAL", "compras", "Abre tu casillero antes de completar tus compras en línea."),
    ("paso-4-rastreo-venezuela.jpg", "¿Listo para cotizar?", "Ten medidas y destino", "cotizacion", "Comparte medidas, peso aproximado, contenido y ciudad de destino."),
]


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    scale = max(size[0] / image.width, size[1] / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def lines_for(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=font)[2] <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def gradient(size: tuple[int, int]) -> Image.Image:
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    pixels = layer.load()
    for y in range(size[1]):
        top = int(210 * max(0, 1 - y / (size[1] * 0.56)))
        bottom = int(150 * max(0, (y - size[1] * 0.72) / (size[1] * 0.28)))
        alpha = max(top, bottom)
        for x in range(size[0]):
            pixels[x, y] = (2, 31, 38, alpha)
    return layer


def build_card(source: Path, output: Path, headline: str, cta: str, *, story: bool) -> None:
    size = (1080, 1920) if story else (1080, 1350)
    image = cover(Image.open(source).convert("RGB"), size)
    image = ImageEnhance.Color(image).enhance(0.92).convert("RGBA")
    image = Image.alpha_composite(image, gradient(size))
    draw = ImageDraw.Draw(image)
    margin = 70
    title_size = 86 if story else 78
    title_font = ImageFont.truetype(str(FONT_BOLD), title_size)
    cta_font = ImageFont.truetype(str(FONT_BOLD), 40 if story else 36)
    small_font = ImageFont.truetype(str(FONT_REGULAR), 25)

    y = 160 if story else 92
    for line in lines_for(draw, headline, title_font, size[0] - margin * 2)[:3]:
        draw.text((margin + 3, y + 4), line, font=title_font, fill=(0, 0, 0, 150))
        draw.text((margin, y), line, font=title_font, fill="white")
        y += title_font.size + 10

    box = draw.textbbox((0, 0), cta, font=cta_font)
    pill_w = min(size[0] - margin * 2, box[2] + 62)
    pill_h = box[3] - box[1] + 36
    pill_y = y + 34
    draw.rounded_rectangle((margin, pill_y, margin + pill_w, pill_y + pill_h), radius=pill_h // 2, fill=(3, 111, 104, 242))
    draw.text((margin + 31, pill_y + 18 - box[1]), cta, font=cta_font, fill="white")

    logo = Image.open(LOGO).convert("RGBA")
    logo.thumbnail((190, 105), Image.Resampling.LANCZOS)
    logo_plate = Image.new("RGBA", (logo.width + 30, logo.height + 22), (255, 255, 255, 235))
    logo_plate.alpha_composite(logo, (15, 11))
    image.alpha_composite(logo_plate, (margin, size[1] - logo_plate.height - 85))
    footer = "varpalcorp.com"
    footer_box = draw.textbbox((0, 0), footer, font=small_font)
    draw.text((size[0] - margin - footer_box[2], size[1] - 58), footer, font=small_font, fill="white")

    output.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output, "JPEG", quality=90, optimize=True, progressive=True)


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
    if len(commit) < 7:
        raise ValueError("Se requiere el SHA del commit que contiene los assets")
    posts: list[dict] = []
    start = date(2026, 10, 11)
    hashtags = ["#VarpalCorp", "#EnviosAVenezuela", "#CasilleroMiami", "#VenezolanosEnUSA", "#MiamiVenezuela"]
    for index, (_source, headline, cta, slug, fact) in enumerate(TOPICS, start=1):
        day = start + timedelta(days=index - 1)
        for media_type, hour, suffix in (("image", "11:00", "feed"), ("story", "19:00", "story")):
            filename = f"{index:02d}-{slug}-{suffix}.jpg"
            url = f"https://raw.githubusercontent.com/latinking26us-hub/varpal-images/{commit}/continuity-2026-10-11/{filename}"
            post = {
                "key": f"continuity-2026-10-d{index:02d}-{suffix}-{slug}",
                "fecha_post": day.isoformat(),
                "hora_post": hour,
                "timezone": "America/New_York",
                "media_type": media_type,
                "filename": filename,
                "image_url": url,
                "asset_sha256": digest(OUT / filename),
                "asset_width": 1080,
                "asset_height": 1350 if media_type == "image" else 1920,
                "proposito": fact,
                "blockers": [],
                "approved": False,
            }
            if media_type == "image":
                post["caption"] = (
                    f"{headline}\n\n{fact}\n\nAntes de enviar, comparte los datos de tu caja para recibir orientación según el contenido y el destino.\n\n"
                    "Escríbenos por WhatsApp 👉 +1 786 448 1426\nAbre tu casillero 👉 varpalcorp.com/casillero"
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
