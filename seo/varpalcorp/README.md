# Kit de posicionamiento — varpalcorp.com (Google + IA)

Objetivo: que `varpalcorp.com` **aparezca en Google** y sea **encontrado y citado por las IA**
(ChatGPT, Perplexity, Gemini, Google AI Overviews, Claude). Esto es SEO + AEO/GEO.

> Estos archivos son para aplicarlos al sitio `varpalcorp.com` (no viven en este repo de imágenes;
> están aquí solo como "staging" versionado para que Codex/tu hosting los tome).

## Contenido del kit
- `robots.txt` → permite Google + rastreadores de IA (GPTBot, ClaudeBot, PerplexityBot, Google-Extended…) + apunta al sitemap.
- `schema-organization.jsonld` → datos de la empresa (para rich results y para que la IA entienda quién eres). Va en el `<head>` de todas las páginas.
- `schema-faq.jsonld` → preguntas frecuentes (Google las muestra como rich snippet y la IA las usa para responder). Va en la página de FAQ o la home.
- `llms.txt` → resumen del negocio pensado para que las IA lo lean. Publicar en `https://varpalcorp.com/llms.txt`.

## Plan priorizado

### Tier 0 — Cerrar la migración (fundamento, primero)
1. **301** de cada URL `.net` → su equivalente `.com` (no solo la home).
2. **Canónica propia** en cada página `.com` (`<link rel="canonical" href="https://varpalcorp.com/...">`).
3. Elegir **un solo host** (www o no-www) y redirigir el otro con 301.
4. Search Console: **Cambio de dirección** (.net → .com) + verificar ambas propiedades.
5. Enviar **sitemap.xml** de `.com` en Search Console.

### Tier 1 — Técnico
- HTTPS en todo, sin contenido mixto.
- `robots.txt` (usar el de este kit) + `sitemap.xml` (todas las URLs importantes).
- Velocidad y móvil (Core Web Vitals): imágenes comprimidas, lazy-load, buen LCP.
- URLs limpias y descriptivas (`/envios-miami-venezuela`, `/casillero-miami`, `/aereo-maritimo`).

### Tier 2 — On-page (por página)
- `<title>` único (50–60 car.) y `meta description` única (150–160 car.).
- Un solo `<h1>` por página + `H2/H3` con las palabras clave.
- `alt` descriptivo en imágenes.
- Enlazado interno entre páginas.
- **Títulos/descriptions sugeridos:**
  - Home: `VARPAL Group | Envíos de Miami a Venezuela puerta a puerta` — "Courier Miami→Venezuela: aéreo, marítimo, casillero en Miami y tracking 24/7. Cotiza por WhatsApp."
  - Casillero: `Casillero en Miami para enviar a Venezuela | VARPAL` — "Compra en USA y recibe en Venezuela. Te damos casillero en Miami, consolidamos y enviamos puerta a puerta."
  - Aéreo/Marítimo: `Envío aéreo y marítimo Miami–Venezuela | VARPAL` — "Aéreo en 3–5 días (salidas viernes) o marítimo para carga voluminosa. Te asesoramos por WhatsApp."

### Tier 3 — Schema / datos estructurados
- Insertar `schema-organization.jsonld` en el `<head>` de todas las páginas.
- Insertar `schema-faq.jsonld` en la FAQ/home.
- (Opcional) `Service` y `BreadcrumbList` por página de servicio.

### Tier 4 — Contenido para IA (AEO/GEO)
- Página **FAQ** real y visible con las mismas preguntas del schema (la IA cita FAQs).
- Contenido claro y factual que responda preguntas ("cómo enviar", "cuánto tarda", "qué se puede enviar") — **sin precios**, redirigir a WhatsApp.
- Publicar **`llms.txt`** en la raíz.
- **NAP consistente** (Nombre, Address, Phone) idéntico en web, Google Business, redes y directorios.

### Tier 5 — Autoridad / off-page (lo que más mueve la aguja local)
- **Google Business Profile** (Perfil de Empresa) — clave para "envíos a Venezuela Miami". Completar y verificar.
- Reseñas de clientes reales.
- Perfiles sociales enlazados (`sameAs` en el schema) y coherentes.
- Altas en directorios de envíos/courier con NAP idéntico.

## Cómo medир
- Google Search Console: cobertura, rendimiento (impresiones/clics), Core Web Vitals.
- Probar el schema en `https://search.google.com/test/rich-results`.
- Buscar en ChatGPT/Perplexity "envíos de Miami a Venezuela" y ver si aparece VARPAL (con el tiempo).

---

## MASTER PROMPT para Codex (aplicar en el sitio varpalcorp.com)

> Pégalo en Codex, en la máquina/repo donde vive el sitio `varpalcorp.com`.

ROL: Optimiza el sitio `varpalcorp.com` para posicionar en Google y para ser citado por IA
(SEO + AEO/GEO). Trabaja sobre el código real del sitio. No inventes datos: usa Nombre
"VARPAL Group Corporation", WhatsApp +1 (786) 448-1426, email info@varpalcorp.com, Miami FL,
Instagram @varpalcorp. NO publiques precios.

TAREAS (en orden):
1. MIGRACIÓN: implementa 301 de todas las URLs de `varpalcorp.net` → su equivalente en
   `varpalcorp.com`; elige un host canónico (www o no-www) y redirige el otro; añade
   `<link rel="canonical">` propio en cada página.
2. robots.txt + sitemap.xml: usa el `robots.txt` del kit (permite Google + IA + Sitemap);
   genera `sitemap.xml` con todas las páginas y súbelo; envíalo en Search Console; haz el
   "Cambio de dirección" .net→.com.
3. HEAD por página: `<title>` y `meta description` únicos (ver sugerencias del kit), un solo
   `<h1>`, y `alt` en imágenes.
4. SCHEMA: inserta el JSON-LD de Organization (todas las páginas) y FAQPage (FAQ/home) del kit.
   Verifica en el Rich Results Test.
5. IA: publica `llms.txt` en la raíz; crea/mejora una página FAQ visible con las mismas
   preguntas del schema.
6. RENDIMIENTO: comprime imágenes, habilita caché/gzip, revisa Core Web Vitals (móvil).

ENTREGABLE: reporta qué cambiaste por página, confirma que el Rich Results Test pasa, que el
301 .net→.com funciona (probar 2–3 URLs), y que Search Console tiene el sitemap + cambio de
dirección. Si algo necesita mi decisión (dirección física real, host www vs no-www, quitar el
.net), pregúntame antes.
