# Panal Negro — Assets Oficiales & Badges de Footer

Repositorio de distribución pública de recursos gráficos, logos, animaciones y badges de atribución de autoría ("Desarrollado por Panal Negro") para incluir en sitios web de clientes y proyectos propios.

Los recursos están optimizados en formato **SVG vectorial con contornos trazados** (sin dependencias de fuentes externas instaladas en el cliente) y se distribuyen globalmente a través del CDN de **jsDelivr** con soporte completo de CORS y compresión Brotli.

---

## 🚀 Cómo usar en tus proyectos (vía CDN)

Reemplazá `<usuario>` por tu usuario u organización de GitHub:

### Opción 1: Badge de Footer directo (`<img>`)
La forma más simple y limpia de colocar la atribución en el footer de cualquier cliente:

```html
<a href="https://panalnegro.com" target="_blank" rel="noopener" aria-label="Desarrollado por Panal Negro">
  <img 
    src="https://cdn.jsdelivr.net/gh/<usuario>/panalnegro-assets@main/badges/badge-dark.svg" 
    alt="Desarrollado por Panal Negro" 
    height="36" 
    loading="lazy" 
  />
</a>
```

### Opción 2: Web Component autónomo (`<panal-negro-badge>`)
Para aislamiento total de estilos CSS mediante Shadow DOM:

```html
<!-- En el <head> o antes de </body> -->
<script src="https://cdn.jsdelivr.net/gh/<usuario>/panalnegro-assets@main/snippets/badge.js" defer></script>

<!-- En el footer -->
<panal-negro-badge theme="dark" variant="badge"></panal-negro-badge>
```
Atributos soportados:
- `theme="dark|light"` (por defecto `dark`)
- `variant="badge|sistemas|desarrollo|compact|minimal"` (por defecto `badge`)
- `animated="true|false"` (activa el pulso sutil de la celda ámbar)

---

## 📦 Catálogo de Recursos

### 1. Badges de Footer (`/badges`)

| Archivo | Variante | Altura | Descripción |
|---|---|---|---|
| `badges/badge-dark.svg` | Oscuro | 36px | Cápsula oscura "Desarrollado por Panal Negro" |
| `badges/badge-light.svg` | Claro | 36px | Cápsula clara para footers blancos |
| `badges/badge-sistemas-dark.svg` | Corporativo | 36px | "Sistemas por Panal Negro" (fondo oscuro) |
| `badges/badge-sistemas-light.svg` | Corporativo | 36px | "Sistemas por Panal Negro" (fondo claro) |
| `badges/badge-desarrollo-dark.svg` | Directo | 36px | "Desarrollo por Panal Negro" (fondo oscuro) |
| `badges/badge-desarrollo-light.svg` | Directo | 36px | "Desarrollo por Panal Negro" (fondo claro) |
| `badges/badge-compact-dark.svg` | Compacto | 36px | Solo Isotipo + PANAL NEGRO en cápsula |
| `badges/badge-compact-light.svg` | Compacto | 36px | Solo Isotipo + PANAL NEGRO en cápsula clara |
| `badges/badge-minimal-dark.svg` | Minimal | 24px | Sin fondo ni borde (transparente) |
| `badges/badge-minimal-light.svg` | Minimal | 24px | Sin fondo ni borde para fondo blanco |
| `badges/badge-animado-dark.svg` | Animado | 36px | Cápsula oscura con celda ámbar latiendo suavemente |
| `badges/badge-animado-light.svg` | Animado | 36px | Cápsula clara con celda ámbar animada |

### 2. Logos Maestros (`/logos`)

| Archivo | Descripción | Uso recomendado |
|---|---|---|
| `logos/horizontal-negativo.svg` | Isotipo crema + ámbar + palabra crema | Fondos negros / oscuros |
| `logos/horizontal-color.svg` | Isotipo negro + ámbar + palabra tinta | Fondos blancos / crema |
| `logos/simbolo-color.svg` | Isotipo 7 celdas con acento ámbar `#F5A524` | Favicones, avatares, cabeceras |
| `logos/simbolo-crema.svg` | Isotipo monocromo crema `#F4EFE6` | Fondos oscuros |
| `logos/simbolo-negro.svg` | Isotipo monocromo tinta `#0C0B09` | Impresión / monocromo |
| `logos/vertical-color.svg` | Isotipo centrado arriba y palabra debajo | Centrados / portadas |

### 3. Animaciones (`/animaciones`)

| Archivo | Tipo | Descripción |
|---|---|---|
| `animaciones/logo-animado.svg` | SVG | Intro de celdas y desplazamiento de palabra |
| `animaciones/simbolo-pulso.svg` | SVG | Celda ámbar con respiración en bucle infinito |
| `animaciones/logo-animado-1080x1080.mp4` | MP4 | Video para redes o presentaciones |

---

## 🛠️ Cómo publicar este repositorio en GitHub

1. Creá un repositorio público en GitHub (por ejemplo, `panalnegro-assets`).
2. En tu terminal local dentro de esta carpeta:
```bash
git init
git add .
git commit -m "feat: initial brand assets, badges and cdn setup"
git branch -M main
git remote add origin https://github.com/<tu-usuario>/panalnegro-assets.git
git push -u origin main
```
3. ¡Listo! A partir de ese momento, jsDelivr empieza a servir tus assets de forma inmediata.

### Control de versiones y caché en producción
Para evitar problemas de caché cuando actualices un logo en el futuro, podés etiquetar versiones con Git:
```bash
git tag v1.0.0
git push origin v1.0.0
```
Y en las webs de tus clientes apuntar a la versión fija:
```html
https://cdn.jsdelivr.net/gh/<usuario>/panalnegro-assets@v1.0.0/badges/badge-dark.svg
```

---

## 👁️ Visor Local Interactivo

Para revisar todos los badges y copiar códigos con 1 click, abrí localmente el archivo `preview.html` en tu navegador.
