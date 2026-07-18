# Estado de publicación nativa Instagram — VARPAL

Última actualización: 2026-06-27 · Responsable: Claude Code (frente Marketing/IG)

## Resumen ejecutivo

**Estado global: BLOCKED** — falta infraestructura pública en `main` + credenciales Meta.

| Componente | Estado |
|---|---|
| Assets editoriales (6 feed VP CORP) | ✅ Listos, renombrados y organizados |
| privacy.html (Meta App Review) | ✅ Reescrito y profesional (`legal/privacy.html`) |
| Repo público | ✅ Sí |
| URL pública estable (assets en `main`) | ⛔ Pendiente: hay que llevar este branch a `main` |
| GitHub Pages | ⛔ No activo (requiere acción de admin) |
| Credenciales Meta (IG_BUSINESS_ACCOUNT_ID, IG_ACCESS_TOKEN) | ⛔ Pendientes (fuera de este repo) |
| Módulo nativo plataforma (`/admin/instagram`) | ❓ Vive en `C:\VARPAL\varpal-platform` — sin acceso desde este entorno |

## Lo que se hizo en este repo (varpal-images)

1. **Auditoría visual** de las 18 imágenes existentes.
2. Se identificó la **línea editorial oficial = VP CORP** (set fotográfico cuadrado).
3. Se **eliminó** el antiguo set plano "VARPAL" navy/cyan (12 diseños / 18 archivos):
   otra identidad + íconos rotos `□` + `SCHED_D` con layout roto. Recuperable en git
   (commits `75cc0d6`, `be4f126`).
4. Se reorganizó el repo (`assets/instagram`, `assets/stories`, `assets/reels-covers`,
   `legal`, `docs`) y se renombraron las 6 piezas con nombres descriptivos.
5. Se documentó la **guía de marca** y el **calendario editorial** con captions.

## URL pública (estrategia)

La Meta Graph API exige `image_url` **público y sin login**. Verificado: `raw.githubusercontent.com`
responde 200 sin login. Opciones:

- **Hoy (sin setup):** raw sobre `main` →
  `https://raw.githubusercontent.com/latinking26us-hub/varpal-images/main/assets/instagram/post-01-compra-online.png`
  (requiere que estos cambios estén en `main`).
- **Recomendado (más estable):** activar **GitHub Pages** desde `main` (carpeta raíz) →
  `https://latinking26us-hub.github.io/varpal-images/assets/instagram/post-01-compra-online.png`
  y la privacy en `https://latinking26us-hub.github.io/varpal-images/legal/privacy.html`.

### Cómo activar GitHub Pages (acción manual de Saúl/Codex — admin)
1. GitHub → repo `varpal-images` → **Settings → Pages**.
2. *Source*: **Deploy from a branch** → Branch: **`main`** → Folder: **`/ (root)`** → Save.
3. Esperar 1–2 min y verificar `https://latinking26us-hub.github.io/varpal-images/legal/privacy.html`.

## Blockers para publicar (orden exacto)

1. **Llevar este branch a `main`** (merge / PR) para que las URLs raw/Pages sirvan los assets.
2. (Opcional pero recomendado) **Activar GitHub Pages**.
3. **Obtener credenciales Meta** y cargarlas en la plataforma (NO en este repo, NO en Notion):
   - `INSTAGRAM_BUSINESS_ACCOUNT_ID`
   - `INSTAGRAM_ACCESS_TOKEN` (con `instagram_basic`, `instagram_content_publish`, y
     acceso a la Página de Facebook vinculada).
   - `INSTAGRAM_PUBLISH_ENABLED=true`
4. **Dry-run** desde la plataforma (`/admin/instagram`): validar image_url pública +
   caption + cuenta IG + respuesta de Meta. (Este módulo está en `varpal-platform`,
   fuera de este entorno.)
5. **Publicación controlada** de 1 pieza, con confirmación explícita de Saúl.

## Fuera de alcance de este entorno

Este entorno remoto solo tiene clonado `varpal-images`. Los archivos de la plataforma
(`services/api/...`, scripts `windows/scripts/*.ps1`, alembic `0059`, etc.) están en
`C:\VARPAL\varpal-platform` y deben revisarse/ejecutarse desde el PC (Codex/Cowork).
