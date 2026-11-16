# Credenciales — Ministerio Jesucristo Rey

Acá están todas las credenciales. Cada vez que se cambia algo y se guarda, GitHub arma los PDFs solo (tarda 1 o 2 minutos) y quedan en la carpeta **`pdf`**, listos para imprimir.

- `pdf/TODAS-las-credenciales.pdf` → todas juntas (frente y dorso intercalados, para imprimir doble faz)
- `pdf/credenciales/` → una por persona
- `pdf/frente.pdf` → solo el frente

---

## Cambiar las fechas o la dirección (para todas)

1. Abrí el archivo **`config.yml`** y tocá el lápiz ✏️ (arriba a la derecha).
2. Cambiá lo que está entre comillas. Por ejemplo:
   ```yaml
   emitido: "01/04/26"
   vence: "01/04/27"
   ```
3. Tocá **Commit changes** (botón verde) y de nuevo **Commit changes**.

Listo: en 1 o 2 minutos se actualizan todas.

## Corregir un nombre o un cargo

1. Abrí **`personas.yml`** y tocá el lápiz ✏️.
2. Buscá a la persona y corregí el texto.
3. **Commit changes**.

## Agregar una credencial nueva

**Paso 1 — Subir la foto**
1. Entrá a la carpeta **`fotos`** → **Add file** → **Upload files**.
2. Arrastrá la foto. Ponele un nombre simple, sin espacios ni acentos: `juan-perez.jpg`
3. **Commit changes**.

La foto conviene que sea de frente, fondo claro, del pecho para arriba, y lo más grande posible (sacada con el celular está bien).

**Paso 2 — Subir la firma**
1. La persona firma con birome negra sobre una hoja blanca. Sacale una foto de cerca, con buena luz.
2. Entrá a la carpeta **`firmas`** → **Add file** → **Upload files** → nombre `juan-perez.jpg` → **Commit changes**.

No hace falta recortarla ni pasarla a blanco: el sistema lo hace solo.

**Paso 3 — Cargar los datos**
1. Abrí **`personas.yml`** → lápiz ✏️.
2. Al final, copiá este bloque y cambiá los datos (respetá los espacios de la izquierda):
   ```yaml
   - nombre: JUAN CARLOS PÉREZ
     cargo: OBRERO
     foto: juan-perez.jpg
     firma: juan-perez.jpg
   ```
3. **Commit changes**.

## Dar de baja una credencial

En `personas.yml` borrá el bloque de esa persona (desde el `-` hasta la línea de `firma`).

## ¿Dónde veo si salió bien?

En la pestaña **Actions**: tilde verde ✅ = PDFs listos. Cruz roja ❌ = algo está mal escrito; entrá y abajo de todo dice qué (por ejemplo, "no encuentro la foto fotos/juan-perez.jpg").

## Imprimir

Abrí el PDF y descargalo (botón de descarga arriba a la derecha). Imprimir al **100% / tamaño real**, sin "ajustar a la página". Medida de la tarjeta: 85,6 × 54 mm (como una tarjeta de crédito); se cambia en `config.yml`.

---

### Qué es fijo y qué no

| Fijo (no se toca) | Cambia por persona | Cambia para todas |
|---|---|---|
| Frente de la tarjeta | Foto | Fechas de emisión y vencimiento |
| Logo, nombre del ministerio, fichero | Nombre | Dirección y teléfono |
| Firmas de presidente y vice | Cargo | |
| Nota de renovación | Firma del titular | |
