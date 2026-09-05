# Flujo de voz en off con ElevenLabs (para ambas unidades)

Tu voz ya está clonada en ElevenLabs. Con eso, producir la voz de un mes entero toma ~30 minutos.

## Paso a paso (por lote, no de uno en uno)

1. Abrir ElevenLabs → **Speech Synthesis** → seleccionar tu voz clonada.
2. Copiar el guion del reel (solo el bloque de "voice over" / "voz en off", sin las acotaciones).
3. Ajustes recomendados:
   - **VARPAL (español, cercano):** Stability ~40–50%, Similarity ~75%. Deja que la voz respire y suene a conversación.
   - **VP PEPTIDES (inglés, sobrio):** Stability ~60–70%, Similarity ~80%. Tono más plano y profesional.
4. Generar → escuchar → si una frase suena rara, regenerar solo esa frase (sale distinta cada vez).
5. Descargar MP3 con nombre claro: `VARPAL_S1_LUN.mp3`, `VPP_W2_COA.mp3`, etc.
6. En CapCut: importar el MP3 → subtítulos automáticos sobre el audio → ajustar clips de b-roll al ritmo de la voz.

## Trucos que mejoran el resultado

- **Puntuación = actuación.** Un punto genera pausa; una coma, media pausa. Los guiones ya vienen
  puntuados para esto — no los pegues como un solo párrafo.
- Para énfasis en una palabra, escríbela entre comas: "y eso, exactamente eso, es la diferencia".
- Los números largos mejor en palabras: "el jueves diecisiete" en vez de "el jueves 17" si la voz los lee mal.
- Genera 2 tomas de cada guion y quédate con la mejor: cuesta segundos y se nota.

## Organización sugerida

```
voz-en-off/
├── varpal/2026-09/      ← un MP3 por reel del mes
└── vppeptides/mes-1/
```

(Los MP3 no hace falta subirlos a este repo — pesan y no se editan. Guárdalos en tu Drive/carpeta local.)
