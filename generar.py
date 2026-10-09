"""Generador completo de assets para el repositorio público de Panal Negro.
Genera logos optimizados, badges vectoriales para footers, animaciones, snippets y vista previa.
"""
import html, importlib.util, math, os, pathlib, shutil
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = pathlib.Path(r"C:/Panal Negro")
DESTINO = ROOT / "panalnegro-assets"
LOGOS_DIR = DESTINO / "logos"
PNG_DIR = LOGOS_DIR / "png"
BADGES_DIR = DESTINO / "badges"
ANIM_DIR = DESTINO / "animaciones"
SNIPPETS_DIR = DESTINO / "snippets"

for d in [DESTINO, LOGOS_DIR, PNG_DIR, BADGES_DIR, ANIM_DIR, SNIPPETS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# 1. Cargar generador maestro de logo y tokens
G2 = ROOT / "Marca/02-visual"
spec = importlib.util.spec_from_file_location("logo", G2 / "_generador/logo.py")
L = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)

NEGRO = "#0C0B09"
CARBON = "#1C1A18"
GRAFITO = "#2D2A26"
PIEDRA_OSCURA = "#46433D"
PIEDRA = "#5F5A52"
ARENA_OSCURA = "#8D887D"
ARENA = "#A9A397"
LINEA = "#DDD5C6"
CREMA = "#F4EFE6"
PAPEL = "#FBF8F2"
AMBAR = "#F5A524"

# Cargar Manrope-Medium para contornos de texto de prefijos
TTF_PATH = ROOT / "Marca/03-piezas/fuentes/Manrope-Medium.ttf"
assert TTF_PATH.exists(), f"No existe {TTF_PATH}"
font = TTFont(TTF_PATH)
glyph_set = font.getGlyphSet()
cmap = font.getBestCmap()
upm = font["head"].unitsPerEm
cap_height = font["OS/2"].sCapHeight or upm * 0.7

def text_to_path(text, target_cap=9.2, track=0.02):
    """Convierte texto en trazado SVG en contornos exactos."""
    k = target_cap / cap_height
    pen = SVGPathPen(glyph_set)
    x = 0
    for ch in text:
        code = ord(ch)
        if code in cmap:
            name = cmap[code]
            glyph_set[name].draw(TransformPen(pen, (k, 0, 0, -k, x, 0)))
            x += glyph_set[name].width * k + track * upm * k
        elif ch == ' ':
            x += (upm * 0.3) * k + track * upm * k
    d = pen.getCommands()
    assert "nan" not in d.lower()
    return d, round(x, 2)

# Prefijos preparados
PREFIJOS = {
    "desarrollado": ("Desarrollado por", *text_to_path("Desarrollado por", 9.2)),
    "desarrollo": ("Desarrollo por", *text_to_path("Desarrollo por", 9.2)),
    "sistemas": ("Sistemas por", *text_to_path("Sistemas por", 9.2)),
    "solo_desarrollo": ("Desarrollo", *text_to_path("Desarrollo", 9.2)),
}

# Geometría del símbolo de Panal Negro
SYM_W_SRC = L.BX1 - L.BX0
SYM_H_SRC = L.BY1 - L.BY0

def render_symbol_group(x_left, y_top, target_h=16.0, base=CREMA, acento=AMBAR, animated=False):
    scale = target_h / SYM_H_SRC
    tx = x_left - L.BX0 * scale
    ty = y_top - L.BY0 * scale
    width = SYM_W_SRC * scale
    
    if animated:
        # Símbolo con clase en celda ámbar
        cells = []
        for i, (px, py) in enumerate(L.POS):
            fill = acento if i == 2 else base
            cls_attr = ' class="pn-amber-cell"' if i == 2 else ''
            cells.append(f'<path d="{L.hexpath(px, py, L.R, L.RAD)}" fill="{fill}"{cls_attr}/>')
        content = "".join(cells)
    else:
        content = L.simbolo(base, acento)
        
    return f'<g transform="translate({tx:.3f} {ty:.3f}) scale({scale:.6f})">{content}</g>', width

def render_brand_word(x_left, baseline_y=22.8, target_cap=10.0, color=CREMA):
    kw = target_cap / 36.0
    width = L.WORD_W * kw
    elem = f'<path transform="translate({x_left:.3f} {baseline_y:.3f}) scale({kw:.6f})" d="{L.WORD_D}" fill="{color}"/>'
    return elem, width

# ----------------------------------------------------
# 2. Generación de Badges para Footers
# ----------------------------------------------------
def build_badge_svg(prefix_key=None, theme="dark", variant="pill", animated=False):
    """Construye un badge SVG en cápsula o minimal."""
    H = 36 if variant == "pill" else 24
    baseline_y = 22.8 if variant == "pill" else 16.5
    sym_y_top = 10.0 if variant == "pill" else 4.0
    sym_h = 16.0
    
    pad_x = 14 if variant == "pill" else 2
    gap_prefix_sym = 10
    gap_sym_word = 7.5
    
    # Colores según tema
    if theme == "dark":
        bg = NEGRO
        border = GRAFITO
        prefix_color = ARENA
        base_sym = CREMA
        word_color = CREMA
    else:
        bg = PAPEL
        border = LINEA
        prefix_color = PIEDRA
        base_sym = NEGRO
        word_color = NEGRO
        
    cursor_x = pad_x
    elements = []
    
    # 1. Prefijo opcional ("Desarrollado por", etc.)
    if prefix_key and prefix_key in PREFIJOS:
        p_label, p_d, p_w = PREFIJOS[prefix_key]
        elements.append(f'<path transform="translate({cursor_x:.3f} {baseline_y:.3f})" d="{p_d}" fill="{prefix_color}"/>')
        cursor_x += p_w + gap_prefix_sym
    
    # 2. Símbolo
    sym_elem, sym_w = render_symbol_group(cursor_x, sym_y_top, target_h=sym_h, base=base_sym, acento=AMBAR, animated=animated)
    elements.append(sym_elem)
    cursor_x += sym_w + gap_sym_word
    
    # 3. Palabra "PANAL NEGRO"
    word_elem, word_w = render_brand_word(cursor_x, baseline_y=baseline_y, target_cap=10.0, color=word_color)
    elements.append(word_elem)
    cursor_x += word_w + pad_x
    
    W = round(cursor_x, 1)
    
    # Fondo si es pill
    bg_svg = ""
    if variant == "pill":
        bg_svg = f'<rect x="0.5" y="0.5" width="{W - 1:.1f}" height="{H - 1:.1f}" rx="17.5" fill="{bg}" stroke="{border}" stroke-width="1"/>'
        
    anim_style = ""
    if animated:
        anim_style = """<style>
  @keyframes pn-pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(0.88); opacity: 0.72; }
  }
  .pn-amber-cell {
    transform-box: fill-box;
    transform-origin: center;
    animation: pn-pulse 2.8s cubic-bezier(0.2, 0, 0, 1) infinite;
  }
  @media (prefers-reduced-motion: reduce) {
    .pn-amber-cell { animation: none; }
  }
</style>"""
        
    title_label = "Panal Negro"
    if prefix_key:
        title_label = f"{PREFIJOS[prefix_key][0]} Panal Negro"
        
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{html.escape(title_label)}">
  <title>{html.escape(title_label)}</title>
  {anim_style}
  {bg_svg}
  {''.join(elements)}
</svg>"""

badges_to_generate = [
    ("badge-dark.svg", "desarrollado", "dark", "pill", False),
    ("badge-light.svg", "desarrollado", "light", "pill", False),
    ("badge-sistemas-dark.svg", "sistemas", "dark", "pill", False),
    ("badge-sistemas-light.svg", "sistemas", "light", "pill", False),
    ("badge-desarrollo-dark.svg", "desarrollo", "dark", "pill", False),
    ("badge-desarrollo-light.svg", "desarrollo", "light", "pill", False),
    ("badge-compact-dark.svg", None, "dark", "pill", False),
    ("badge-compact-light.svg", None, "light", "pill", False),
    ("badge-minimal-dark.svg", "desarrollado", "dark", "minimal", False),
    ("badge-minimal-light.svg", "desarrollado", "light", "minimal", False),
    ("badge-animado-dark.svg", "desarrollado", "dark", "pill", True),
    ("badge-animado-light.svg", "desarrollado", "light", "pill", True),
]

for filename, pref, theme, var, anim in badges_to_generate:
    svg_content = build_badge_svg(pref, theme, var, anim)
    (BADGES_DIR / filename).write_text(svg_content.strip() + "\n", encoding="utf-8")

# ----------------------------------------------------
# 3. Copiar Logos Oficiales SVG
# ----------------------------------------------------
SRC_LOGOS = ROOT / "Kit/logo"
logos_copiar = [
    "simbolo-color.svg", "simbolo-negro.svg", "simbolo-crema.svg", "simbolo-negativo.svg",
    "horizontal-color.svg", "horizontal-negro.svg", "horizontal-crema.svg", "horizontal-negativo.svg",
    "vertical-color.svg", "vertical-negro.svg", "vertical-crema.svg", "vertical-negativo.svg",
    "fragmento-color.svg", "fragmento-negro.svg", "fragmento-crema.svg", "fragmento-negativo.svg"
]
for l in logos_copiar:
    src_file = SRC_LOGOS / l
    if src_file.exists():
        shutil.copy2(src_file, LOGOS_DIR / l)

# ----------------------------------------------------
# 4. Copiar PNGs de Alta Resolución
# ----------------------------------------------------
pngs_copiar = [
    (ROOT / "Kit/avatares/avatar-negro-1080.png", "avatar-negro-1080.png"),
    (ROOT / "Kit/avatares/avatar-crema-1080.png", "avatar-crema-1080.png"),
    (ROOT / "Kit/favicon/icon-512.png", "icon-512.png"),
    (ROOT / "Kit/favicon/icon-192.png", "icon-192.png"),
    (ROOT / "Kit/favicon/apple-touch-icon.png", "apple-touch-icon.png"),
    (ROOT / "Kit/favicon/favicon-32.png", "favicon-32.png"),
    (ROOT / "Kit/portadas/og-1200x630.png", "og-1200x630.png"),
]
for src_p, dst_name in pngs_copiar:
    if src_p.exists():
        shutil.copy2(src_p, PNG_DIR / dst_name)

# ----------------------------------------------------
# 5. Animaciones
# ----------------------------------------------------
# Símbolo con pulso ámbar en bucle (256x256)
def build_simbolo_pulso():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-label="Panal Negro — símbolo animado">
  <title>Panal Negro — símbolo animado</title>
  <style>
    @keyframes pn-pulse {{
      0%, 100% {{ transform: scale(1); opacity: 1; }}
      50% {{ transform: scale(0.88); opacity: 0.72; }}
    }}
    .pn-amber-cell {{
      transform-box: fill-box;
      transform-origin: center;
      animation: pn-pulse 2.8s cubic-bezier(0.2, 0, 0, 1) infinite;
    }}
    @media (prefers-reduced-motion: reduce) {{
      .pn-amber-cell {{ animation: none; }}
    }}
  </style>
  <path d="{L.hexpath(L.POS[0][0], L.POS[0][1], L.R, L.RAD)}" fill="{NEGRO}"/>
  <path d="{L.hexpath(L.POS[1][0], L.POS[1][1], L.R, L.RAD)}" fill="{NEGRO}"/>
  <path class="pn-amber-cell" d="{L.hexpath(L.POS[2][0], L.POS[2][1], L.R, L.RAD)}" fill="{AMBAR}"/>
  <path d="{L.hexpath(L.POS[3][0], L.POS[3][1], L.R, L.RAD)}" fill="{NEGRO}"/>
  <path d="{L.hexpath(L.POS[4][0], L.POS[4][1], L.R, L.RAD)}" fill="{NEGRO}"/>
  <path d="{L.hexpath(L.POS[5][0], L.POS[5][1], L.R, L.RAD)}" fill="{NEGRO}"/>
  <path d="{L.hexpath(L.POS[6][0], L.POS[6][1], L.R, L.RAD)}" fill="{NEGRO}"/>
</svg>"""

(ANIM_DIR / "simbolo-pulso.svg").write_text(build_simbolo_pulso().strip() + "\n", encoding="utf-8")

# Logo animado existente
SRC_ANIM = ROOT / "Marca/04-movimiento/logo-animado"
if (SRC_ANIM / "logo-animado.svg").exists():
    shutil.copy2(SRC_ANIM / "logo-animado.svg", ANIM_DIR / "logo-animado.svg")
if (SRC_ANIM / "logo-animado-1080x1080.mp4").exists():
    shutil.copy2(SRC_ANIM / "logo-animado-1080x1080.mp4", ANIM_DIR / "logo-animado-1080x1080.mp4")

# ----------------------------------------------------
# 6. Snippets
# ----------------------------------------------------
# Web Component badge.js
BADGE_JS = """/**
 * Panal Negro · Footer Badge Web Component
 * Uso:
 *   <script src="https://cdn.jsdelivr.net/gh/<usuario>/<repo>@main/snippets/badge.js" defer></script>
 *   <panal-negro-badge theme="dark" variant="badge" href="https://panalnegro.com"></panal-negro-badge>
 */
class PanalNegroBadge extends HTMLElement {
  connectedCallback() {
    const theme = this.getAttribute('theme') || 'dark';
    const variant = this.getAttribute('variant') || 'badge'; // 'badge' | 'sistemas' | 'desarrollo' | 'compact' | 'minimal'
    const href = this.getAttribute('href') || 'https://panalnegro.com';
    const animated = this.hasAttribute('animated') || this.getAttribute('animated') === 'true';

    let file = 'badge-dark.svg';
    if (variant === 'sistemas') file = theme === 'light' ? 'badge-sistemas-light.svg' : 'badge-sistemas-dark.svg';
    else if (variant === 'desarrollo') file = theme === 'light' ? 'badge-desarrollo-light.svg' : 'badge-desarrollo-dark.svg';
    else if (variant === 'compact') file = theme === 'light' ? 'badge-compact-light.svg' : 'badge-compact-dark.svg';
    else if (variant === 'minimal') file = theme === 'light' ? 'badge-minimal-light.svg' : 'badge-minimal-dark.svg';
    else if (animated) file = theme === 'light' ? 'badge-animado-light.svg' : 'badge-animado-dark.svg';
    else file = theme === 'light' ? 'badge-light.svg' : 'badge-dark.svg';

    // Determina la base CDN del propio script o fallback
    let cdnBase = 'https://cdn.jsdelivr.net/gh/panalnegro/panalnegro-assets@main';
    const currentScript = document.currentScript || Array.from(document.querySelectorAll('script')).find(s => s.src && s.src.includes('badge.js'));
    if (currentScript && currentScript.src) {
      try {
        const url = new URL(currentScript.src);
        const parts = url.pathname.split('/snippets/')[0];
        cdnBase = url.origin + parts;
      } catch (e) {}
    }

    const badgeUrl = `${cdnBase}/badges/${file}`;

    const shadow = this.attachShadow({ mode: 'open' });
    shadow.innerHTML = `
      <style>
        :host { display: inline-block; vertical-align: middle; }
        a {
          display: inline-flex;
          align-items: center;
          text-decoration: none;
          outline: none;
          transition: transform 120ms cubic-bezier(0.2, 0, 0, 1), opacity 120ms cubic-bezier(0.2, 0, 0, 1);
        }
        a:hover {
          transform: translateY(-1px);
          opacity: 0.95;
        }
        a:focus-visible {
          border-radius: 999px;
          outline: 2px solid #F5A524;
          outline-offset: 3px;
        }
        img { display: block; height: ${variant === 'minimal' ? '24px' : '36px'}; width: auto; }
      </style>
      <a href="${href}" target="_blank" rel="noopener" aria-label="Desarrollado por Panal Negro">
        <img src="${badgeUrl}" alt="Panal Negro" loading="lazy" />
      </a>
    `;
  }
}
if (!customElements.get('panal-negro-badge')) {
  customElements.define('panal-negro-badge', PanalNegroBadge);
}
"""
(SNIPPETS_DIR / "badge.js").write_text(BADGE_JS.strip() + "\n", encoding="utf-8")

# Snippets HTML footer-badge.html
FOOTER_SNIPPETS = """<!-- Panal Negro · Ejemplos de integración en footers de sitios web -->

<!-- ================================================================= -->
<!-- OPCIÓN 1: La más directa (Tag <img> con CDN jsDelivr)            -->
<!-- Reemplazá <usuario> por tu usuario u organización de GitHub        -->
<!-- ================================================================= -->

<!-- Variante Fondo Oscuro (Cápsula estándar) -->
<a href="https://panalnegro.com" target="_blank" rel="noopener" aria-label="Desarrollado por Panal Negro" style="display:inline-block; text-decoration:none; transition:opacity .15s ease;">
  <img 
    src="https://cdn.jsdelivr.net/gh/<usuario>/panalnegro-assets@main/badges/badge-dark.svg" 
    alt="Desarrollado por Panal Negro" 
    height="36" 
    loading="lazy"
    style="display:block; height:36px; width:auto;"
  />
</a>

<!-- Variante Fondo Claro (Cápsula clara) -->
<a href="https://panalnegro.com" target="_blank" rel="noopener" aria-label="Desarrollado por Panal Negro" style="display:inline-block; text-decoration:none; transition:opacity .15s ease;">
  <img 
    src="https://cdn.jsdelivr.net/gh/<usuario>/panalnegro-assets@main/badges/badge-light.svg" 
    alt="Desarrollado por Panal Negro" 
    height="36" 
    loading="lazy"
    style="display:block; height:36px; width:auto;"
  />
</a>


<!-- ================================================================= -->
<!-- OPCIÓN 2: Componente HTML + CSS liviano con micro-interacción    -->
<!-- Ideal si querés controlar el hover o integrarlo con Tailwind/CSS  -->
<!-- ================================================================= -->

<style>
  .pn-footer-link {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 999px;
    background: #0C0B09;
    border: 1px solid #2D2A26;
    color: #A9A397;
    font-family: 'Manrope', system-ui, -apple-system, sans-serif;
    font-size: 11px;
    font-weight: 500;
    text-decoration: none;
    line-height: 1;
    transition: transform 120ms cubic-bezier(0.2, 0, 0, 1), border-color 120ms cubic-bezier(0.2, 0, 0, 1), color 120ms cubic-bezier(0.2, 0, 0, 1);
  }
  .pn-footer-link:hover {
    transform: translateY(-1px);
    border-color: #46433D;
    color: #F4EFE6;
  }
  .pn-footer-link img {
    height: 16px;
    width: auto;
    display: block;
  }
  .pn-footer-link strong {
    color: #F4EFE6;
    font-weight: 600;
    font-size: 12px;
    letter-spacing: 0.02em;
  }
</style>

<a href="https://panalnegro.com" target="_blank" rel="noopener" class="pn-footer-link">
  <span>Desarrollo</span>
  <img src="https://cdn.jsdelivr.net/gh/<usuario>/panalnegro-assets@main/logos/simbolo-color.svg" alt="" aria-hidden="true" />
  <strong>PANAL NEGRO</strong>
</a>


<!-- ================================================================= -->
<!-- OPCIÓN 3: Web Component encapsulado (Shadow DOM, 0 colisiones CSS) -->
<!-- ================================================================= -->

<!-- Importar script (una sola vez en el <head> o antes de cerrar <body>) -->
<script src="https://cdn.jsdelivr.net/gh/<usuario>/panalnegro-assets@main/snippets/badge.js" defer></script>

<!-- Insertar el elemento donde quieras que aparezca -->
<panal-negro-badge theme="dark" variant="badge"></panal-negro-badge>

<!-- O versión minimalista para fondo claro: -->
<!-- <panal-negro-badge theme="light" variant="minimal"></panal-negro-badge> -->
"""
(SNIPPETS_DIR / "footer-badge.html").write_text(FOOTER_SNIPPETS.strip() + "\n", encoding="utf-8")

# ----------------------------------------------------
# 7. Visor Interactivo preview.html
# ----------------------------------------------------
PREVIEW_HTML = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Panal Negro · Catálogo de Assets & Badges de Footer</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Manrope:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --pn-negro: #0C0B09;
      --pn-carbon: #1C1A18;
      --pn-grafito: #2D2A26;
      --pn-piedra-oscura: #46433D;
      --pn-piedra: #5F5A52;
      --pn-arena-oscura: #8D887D;
      --pn-arena: #A9A397;
      --pn-linea: #DDD5C6;
      --pn-crema: #F4EFE6;
      --pn-papel: #FBF8F2;
      --pn-ambar: #F5A524;
      --pn-dur: 120ms;
      --pn-ease: cubic-bezier(0.2, 0, 0, 1);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--pn-negro);
      color: var(--pn-crema);
      font-family: 'Manrope', system-ui, sans-serif;
      line-height: 1.5;
      padding: 40px 24px 80px;
      -webkit-font-smoothing: antialiased;
    }
    .wrap { max-width: 1120px; margin: 0 auto; }
    header {
      padding-bottom: 32px;
      border-bottom: 1px solid var(--pn-grafito);
      margin-bottom: 40px;
    }
    .tag {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--pn-ambar);
      display: inline-block;
      margin-bottom: 8px;
    }
    h1 {
      font-size: 32px;
      font-weight: 600;
      letter-spacing: -0.02em;
      color: var(--pn-papel);
      margin-bottom: 12px;
    }
    p.lead {
      color: var(--pn-arena);
      font-size: 16px;
      max-width: 720px;
      margin-bottom: 24px;
    }
    
    /* Config Bar */
    .config-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 16px;
      background: var(--pn-carbon);
      border: 1px solid var(--pn-grafito);
      padding: 16px 20px;
      border-radius: 12px;
      margin-bottom: 40px;
    }
    .config-label {
      font-size: 13px;
      font-weight: 500;
      color: var(--pn-arena);
    }
    .config-input {
      background: var(--pn-negro);
      border: 1px solid var(--pn-piedra-oscura);
      border-radius: 6px;
      padding: 8px 12px;
      color: var(--pn-papel);
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      width: 200px;
    }
    .config-input:focus {
      outline: 2px solid var(--pn-ambar);
      border-color: transparent;
    }
    .theme-picker {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-left: auto;
    }
    .theme-btn {
      padding: 6px 12px;
      border-radius: 6px;
      border: 1px solid var(--pn-grafito);
      background: var(--pn-negro);
      color: var(--pn-arena);
      font-size: 12px;
      cursor: pointer;
      font-family: inherit;
      transition: all var(--pn-dur) var(--pn-ease);
    }
    .theme-btn.active, .theme-btn:hover {
      background: var(--pn-piedra-oscura);
      color: var(--pn-papel);
      border-color: var(--pn-arena-oscura);
    }

    /* Sections */
    section { margin-bottom: 56px; }
    h2 {
      font-size: 20px;
      font-weight: 600;
      color: var(--pn-papel);
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    h2 .badge-cnt {
      font-size: 11px;
      font-family: 'JetBrains Mono', monospace;
      padding: 2px 8px;
      border-radius: 999px;
      background: var(--pn-carbon);
      color: var(--pn-ambar);
      border: 1px solid var(--pn-grafito);
    }
    p.sec-sub {
      color: var(--pn-arena);
      font-size: 14px;
      margin-bottom: 20px;
    }

    /* Grilla de items */
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
      gap: 16px;
    }
    .card {
      background: var(--pn-carbon);
      border: 1px solid var(--pn-grafito);
      border-radius: 10px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: border-color var(--pn-dur) var(--pn-ease);
    }
    .card:hover { border-color: var(--pn-piedra-oscura); }
    .card-canvas {
      padding: 28px 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 110px;
      transition: background var(--pn-dur) var(--pn-ease);
    }
    /* Lienzos dinámicos */
    .canvas-negro { background: #0C0B09; }
    .canvas-crema { background: #F4EFE6; }
    .canvas-blanco { background: #FFFFFF; }
    .canvas-carbon { background: #1C1A18; }
    .canvas-zinc { background: #18181B; }

    .card-meta {
      padding: 14px 16px;
      border-top: 1px solid var(--pn-grafito);
      background: rgba(12, 11, 9, 0.4);
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: auto;
    }
    .card-title {
      font-size: 13px;
      font-weight: 600;
      color: var(--pn-papel);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .card-file {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: var(--pn-arena-oscura);
    }
    .card-actions {
      display: flex;
      gap: 8px;
      margin-top: 4px;
    }
    .btn {
      flex: 1;
      padding: 7px 10px;
      border-radius: 6px;
      border: 1px solid var(--pn-grafito);
      background: var(--pn-negro);
      color: var(--pn-arena);
      font-size: 11px;
      font-weight: 500;
      cursor: pointer;
      font-family: inherit;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all var(--pn-dur) var(--pn-ease);
    }
    .btn:hover {
      background: var(--pn-piedra-oscura);
      color: var(--pn-papel);
      border-color: var(--pn-arena-oscura);
    }
    .btn.copied {
      background: #14532D;
      color: #86EFAC;
      border-color: #22C55E;
    }

    /* Simulador de Footer */
    .footer-sim {
      background: #141311;
      border: 1px solid var(--pn-grafito);
      border-radius: 12px;
      padding: 40px;
      margin-top: 24px;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }
    .footer-sim-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: var(--pn-piedra);
      font-size: 13px;
      border-bottom: 1px solid var(--pn-grafito);
      padding-bottom: 24px;
    }
    .footer-sim-bottom {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }
    .footer-sim-copy {
      color: var(--pn-arena-oscura);
      font-size: 13px;
    }

    /* Toast */
    #toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--pn-papel);
      color: var(--pn-negro);
      padding: 10px 18px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      transform: translateY(100px);
      opacity: 0;
      transition: all 200ms var(--pn-ease);
      pointer-events: none;
      z-index: 1000;
    }
    #toast.show {
      transform: translateY(0);
      opacity: 1;
    }
  </style>
</head>
<body>
<div class="wrap">
  <header>
    <span class="tag">Panal Negro · Brand Assets CDN</span>
    <h1>Catálogo de Assets & Badges de Footer</h1>
    <p class="lead">
      Recursos oficiales de la marca listos para consumir vía CDN (jsDelivr) en sitios web de clientes y proyectos propios sin problemas de CORS ni compresión.
    </p>

    <div class="config-bar">
      <label class="config-label" for="ghUser">Usuario / Org de GitHub:</label>
      <input type="text" id="ghUser" class="config-input" value="panalnegro" spellcheck="false" />

      <label class="config-label" for="ghRepo" style="margin-left: 12px;">Repo:</label>
      <input type="text" id="ghRepo" class="config-input" value="panalnegro-assets" spellcheck="false" />

      <div class="theme-picker">
        <span class="config-label">Fondo de muestra:</span>
        <button class="theme-btn active" data-canvas="canvas-negro">Negro</button>
        <button class="theme-btn" data-canvas="canvas-carbon">Carbón</button>
        <button class="theme-btn" data-canvas="canvas-zinc">Zinc</button>
        <button class="theme-btn" data-canvas="canvas-crema">Crema</button>
        <button class="theme-btn" data-canvas="canvas-blanco">Blanco</button>
      </div>
    </div>
  </header>

  <!-- SECCIÓN 1: BADGES DE FOOTER -->
  <section>
    <h2>Badges para Footers <span class="badge-cnt">12 versiones</span></h2>
    <p class="sec-sub">Diseñados a altura óptica estandarizada (36px cápsula / 24px minimal) con vectorizado exacto sin dependencias de fuentes externas.</p>

    <div class="grid">
      <!-- 1. badge-dark -->
      <div class="card">
        <div class="card-canvas canvas-negro"><img src="badges/badge-dark.svg" alt="" height="36" /></div>
        <div class="card-meta">
          <div class="card-title">Desarrollado por (Oscuro) <span class="card-file">badge-dark.svg</span></div>
          <div class="card-actions">
            <button class="btn" onclick="copyCdn('badges/badge-dark.svg')">Copiar URL CDN</button>
            <button class="btn" onclick="copyImgTag('badges/badge-dark.svg', 36)">Copiar &lt;img&gt;</button>
          </div>
        </div>
      </div>

      <!-- 2. badge-light -->
      <div class="card">
        <div class="card-canvas canvas-blanco"><img src="badges/badge-light.svg" alt="" height="36" /></div>
        <div class="card-meta">
          <div class="card-title">Desarrollado por (Claro) <span class="card-file">badge-light.svg</span></div>
          <div class="card-actions">
            <button class="btn" onclick="copyCdn('badges/badge-light.svg')">Copiar URL CDN</button>
            <button class="btn" onclick="copyImgTag('badges/badge-light.svg', 36)">Copiar &lt;img&gt;</button>
          </div>
        </div>
      </div>

      <!-- 3. badge-sistemas-dark -->
      <div class="card">
        <div class="card-canvas canvas-negro"><img src="badges/badge-sistemas-dark.svg" alt="" height="36" /></div>
        <div class="card-meta">
          <div class="card-title">Sistemas por (Oscuro) <span class="card-file">badge-sistemas-dark.svg</span></div>
          <div class="card-actions">
            <button class="btn" onclick="copyCdn('badges/badge-sistemas-dark.svg')">Copiar URL CDN</button>
            <button class="btn" onclick="copyImgTag('badges/badge-sistemas-dark.svg', 36)">Copiar &lt;img&gt;</button>
          </div>
        </div>
      </div>

      <!-- 4. badge-sistemas-light -->
      <div class="card">
        <div class="card-canvas canvas-blanco"><img src="badges/badge-sistemas-light.svg" alt="" height="36" /></div>
        <div class="card-meta">
          <div class="card-title">Sistemas por (Claro) <span class="card-file">badge-sistemas-light.svg</span></div>
          <div class="card-actions">
            <button class="btn" onclick="copyCdn('badges/badge-sistemas-light.svg')">Copiar URL CDN</button>
            <button class="btn" onclick="copyImgTag('badges/badge-sistemas-light.svg', 36)">Copiar &lt;img&gt;</button>
          </div>
        </div>
      </div>

      <!-- 5. badge-desarrollo-dark -->
      <div class="card">
        <div class="card-canvas canvas-negro"><img src="badges/badge-desarrollo-dark.svg" alt="" height="36" /></div>
        <div class="card-meta">
          <div class="card-title">Desarrollo por (Oscuro) <span class="card-file">badge-desarrollo-dark.svg</span></div>
          <div class="card-actions">
            <button class="btn" onclick="copyCdn('badges/badge-desarrollo-dark.svg')">Copiar URL CDN</button>
            <button class="btn" onclick="copyImgTag('badges/badge-desarrollo-dark.svg', 36)">Copiar &lt;img&gt;</button>
          </div>
        </div>
      </div>

      <!-- 6. badge-desarrollo-light -->
      <div class="card">
        <div class="card-canvas canvas-blanco"><img src="badges/badge-desarrollo-light.svg" alt="" height="36" /></div>
        <div class="card-meta">
          <div class="card-title">Desarrollo por (Claro) <span class="card-file">badge-desarrollo-light.svg</span></div>
          <div class="card-actions">
            <button class="btn" onclick="copyCdn('badges/badge-desarrollo-light.svg')">Copiar URL CDN</button>
            <button class="btn" onclick="copyImgTag('badges/badge-desarrollo-light.svg', 36)">Copiar &lt;img&gt;</button>
          </div>
        </div>
      </div>

      <!-- 7. badge-compact-dark -->
      <div class="card">
        <div class="card-canvas canvas-negro"><img src="badges/badge-compact-dark.svg" alt="" height="36" /></div>
        <div class="card-meta">
          <div class="card-title">Compacto Logo (Oscuro) <span class="card-file">badge-compact-dark.svg</span></div>
          <div class="card-actions">
            <button class="btn" onclick="copyCdn('badges/badge-compact-dark.svg')">Copiar URL CDN</button>
            <button class="btn" onclick="copyImgTag('badges/badge-compact-dark.svg', 36)">Copiar &lt;img&gt;</button>
          </div>
        </div>
      </div>

      <!-- 8. badge-compact-light -->
      <div class="card">
        <div class="card-canvas canvas-blanco"><img src="badges/badge-compact-light.svg" alt="" height="36" /></div>
        <div class="card-meta">
          <div class="card-title">Compacto Logo (Claro) <span class="card-file">badge-compact-light.svg</span></div>
          <div class="card-actions">
            <button class="btn" onclick="copyCdn('badges/badge-compact-light.svg')">Copiar URL CDN</button>
            <button class="btn" onclick="copyImgTag('badges/badge-compact-light.svg', 36)">Copiar &lt;img&gt;</button>
          </div>
        </div>
      </div>

      <!-- 9. badge-minimal-dark -->
      <div class="card">
        <div class="card-canvas canvas-negro"><img src="badges/badge-minimal-dark.svg" alt="" height="24" /></div>
        <div class="card-meta">
          <div class="card-title">Minimal / Transparente (Oscuro) <span class="card-file">badge-minimal-dark.svg</span></div>
          <div class="card-actions">
            <button class="btn" onclick="copyCdn('badges/badge-minimal-dark.svg')">Copiar URL CDN</button>
            <button class="btn" onclick="copyImgTag('badges/badge-minimal-dark.svg', 24)">Copiar &lt;img&gt;</button>
          </div>
        </div>
      </div>

      <!-- 10. badge-minimal-light -->
      <div class="card">
        <div class="card-canvas canvas-blanco"><img src="badges/badge-minimal-light.svg" alt="" height="24" /></div>
        <div class="card-meta">
          <div class="card-title">Minimal / Transparente (Claro) <span class="card-file">badge-minimal-light.svg</span></div>
          <div class="card-actions">
            <button class="btn" onclick="copyCdn('badges/badge-minimal-light.svg')">Copiar URL CDN</button>
            <button class="btn" onclick="copyImgTag('badges/badge-minimal-light.svg', 24)">Copiar &lt;img&gt;</button>
          </div>
        </div>
      </div>

      <!-- 11. badge-animado-dark -->
      <div class="card">
        <div class="card-canvas canvas-negro"><img src="badges/badge-animado-dark.svg" alt="" height="36" /></div>
        <div class="card-meta">
          <div class="card-title">Animado con Pulso (Oscuro) <span class="card-file">badge-animado-dark.svg</span></div>
          <div class="card-actions">
            <button class="btn" onclick="copyCdn('badges/badge-animado-dark.svg')">Copiar URL CDN</button>
            <button class="btn" onclick="copyImgTag('badges/badge-animado-dark.svg', 36)">Copiar &lt;img&gt;</button>
          </div>
        </div>
      </div>

      <!-- 12. badge-animado-light -->
      <div class="card">
        <div class="card-canvas canvas-blanco"><img src="badges/badge-animado-light.svg" alt="" height="36" /></div>
        <div class="card-meta">
          <div class="card-title">Animado con Pulso (Claro) <span class="card-file">badge-animado-light.svg</span></div>
          <div class="card-actions">
            <button class="btn" onclick="copyCdn('badges/badge-animado-light.svg')">Copiar URL CDN</button>
            <button class="btn" onclick="copyImgTag('badges/badge-animado-light.svg', 36)">Copiar &lt;img&gt;</button>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- SECCIÓN 2: LOGOS MAESTROS -->
  <section>
    <h2>Logos Oficiales SVG <span class="badge-cnt">Vectorial</span></h2>
    <p class="sec-sub">Formatos maestros de la marca para barras de navegación, cabeceras o presentaciones.</p>

    <div class="grid">
      <div class="card">
        <div class="card-canvas canvas-negro"><img src="logos/horizontal-negativo.svg" alt="" height="28" /></div>
        <div class="card-meta">
          <div class="card-title">Horizontal Crema / Ámbar <span class="card-file">horizontal-negativo.svg</span></div>
          <div class="card-actions"><button class="btn" onclick="copyCdn('logos/horizontal-negativo.svg')">Copiar URL CDN</button></div>
        </div>
      </div>

      <div class="card">
        <div class="card-canvas canvas-blanco"><img src="logos/horizontal-color.svg" alt="" height="28" /></div>
        <div class="card-meta">
          <div class="card-title">Horizontal Tinta / Ámbar <span class="card-file">horizontal-color.svg</span></div>
          <div class="card-actions"><button class="btn" onclick="copyCdn('logos/horizontal-color.svg')">Copiar URL CDN</button></div>
        </div>
      </div>

      <div class="card">
        <div class="card-canvas canvas-crema"><img src="logos/simbolo-color.svg" alt="" height="44" /></div>
        <div class="card-meta">
          <div class="card-title">Símbolo Color (Tinta/Ámbar) <span class="card-file">simbolo-color.svg</span></div>
          <div class="card-actions"><button class="btn" onclick="copyCdn('logos/simbolo-color.svg')">Copiar URL CDN</button></div>
        </div>
      </div>

      <div class="card">
        <div class="card-canvas canvas-negro"><img src="logos/simbolo-crema.svg" alt="" height="44" /></div>
        <div class="card-meta">
          <div class="card-title">Símbolo Monocromo Crema <span class="card-file">simbolo-crema.svg</span></div>
          <div class="card-actions"><button class="btn" onclick="copyCdn('logos/simbolo-crema.svg')">Copiar URL CDN</button></div>
        </div>
      </div>

      <div class="card">
        <div class="card-canvas canvas-negro"><img src="logos/simbolo-negativo.svg" alt="" height="44" /></div>
        <div class="card-meta">
          <div class="card-title">Símbolo Negativo (Crema/Ámbar) <span class="card-file">simbolo-negativo.svg</span></div>
          <div class="card-actions"><button class="btn" onclick="copyCdn('logos/simbolo-negativo.svg')">Copiar URL CDN</button></div>
        </div>
      </div>

      <div class="card">
        <div class="card-canvas canvas-negro"><img src="logos/vertical-negativo.svg" alt="" height="54" /></div>
        <div class="card-meta">
          <div class="card-title">Vertical Negativo <span class="card-file">vertical-negativo.svg</span></div>
          <div class="card-actions"><button class="btn" onclick="copyCdn('logos/vertical-negativo.svg')">Copiar URL CDN</button></div>
        </div>
      </div>
    </div>
  </section>

  <!-- SECCIÓN 3: ANIMACIONES -->
  <section>
    <h2>Animaciones de Marca <span class="badge-cnt">SVG & MP4</span></h2>
    <p class="sec-sub">Animaciones puras sin dependencias de JavaScript.</p>

    <div class="grid">
      <div class="card">
        <div class="card-canvas canvas-negro"><img src="animaciones/simbolo-pulso.svg" alt="" height="56" /></div>
        <div class="card-meta">
          <div class="card-title">Símbolo con Pulso Ámbar <span class="card-file">simbolo-pulso.svg</span></div>
          <div class="card-actions"><button class="btn" onclick="copyCdn('animaciones/simbolo-pulso.svg')">Copiar URL CDN</button></div>
        </div>
      </div>

      <div class="card">
        <div class="card-canvas canvas-negro"><img src="animaciones/logo-animado.svg" alt="" height="32" /></div>
        <div class="card-meta">
          <div class="card-title">Logo con Intro de Celdas <span class="card-file">logo-animado.svg</span></div>
          <div class="card-actions"><button class="btn" onclick="copyCdn('animaciones/logo-animado.svg')">Copiar URL CDN</button></div>
        </div>
      </div>
    </div>
  </section>

  <!-- SECCIÓN 4: SIMULADOR DE FOOTER -->
  <section>
    <h2>Simulador de Footer</h2>
    <p class="sec-sub">Vista previa de cómo se integra el badge en un footer real de un sitio de cliente.</p>

    <div class="footer-sim">
      <div class="footer-sim-top">
        <span>Empresa Cliente S.A. — Gestión Operativa</span>
        <span>contacto@cliente.com</span>
      </div>
      <div class="footer-sim-bottom">
        <div class="footer-sim-copy">© 2026 Empresa Cliente S.A. Todos los derechos reservados.</div>
        <a href="https://panalnegro.com" target="_blank" rel="noopener" style="text-decoration:none;">
          <img src="badges/badge-dark.svg" alt="Desarrollado por Panal Negro" height="36" />
        </a>
      </div>
    </div>
  </section>
</div>

<div id="toast">Copiado al portapapeles</div>

<script>
  function getCdnUrl(relPath) {
    const user = document.getElementById('ghUser').value.trim() || 'panalnegro';
    const repo = document.getElementById('ghRepo').value.trim() || 'panalnegro-assets';
    return `https://cdn.jsdelivr.net/gh/${user}/${repo}@main/${relPath}`;
  }

  function showToast(text) {
    const t = document.getElementById('toast');
    t.innerText = text;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2000);
  }

  function copyText(val, msg = 'Copiado al portapapeles') {
    navigator.clipboard.writeText(val).then(() => showToast(msg));
  }

  function copyCdn(path) {
    copyText(getCdnUrl(path), 'URL jsDelivr copiada');
  }

  function copyImgTag(path, h) {
    const url = getCdnUrl(path);
    const snippet = `<a href="https://panalnegro.com" target="_blank" rel="noopener" aria-label="Desarrollado por Panal Negro">\\n  <img src="${url}" alt="Desarrollado por Panal Negro" height="${h}" loading="lazy" />\\n</a>`;
    copyText(snippet, 'Código <img> copiado');
  }

  // Cambio interactivo de fondos de canvas
  document.querySelectorAll('.theme-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.theme-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cls = btn.dataset.canvas;
      document.querySelectorAll('.card-canvas').forEach(c => {
        c.className = 'card-canvas ' + cls;
      });
    });
  });
</script>
</body>
</html>
"""
(DESTINO / "preview.html").write_text(PREVIEW_HTML.strip() + "\n", encoding="utf-8")

# ----------------------------------------------------
# 8. README.md & .gitignore
# ----------------------------------------------------
GITIGNORE = """# Gitignore para panalnegro-assets
.DS_Store
Thumbs.db
*.tmp
*~
"""
(DESTINO / ".gitignore").write_text(GITIGNORE.strip() + "\n", encoding="utf-8")

README_MD = """# Panal Negro — Assets Oficiales & Badges de Footer

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
"""
(DESTINO / "README.md").write_text(README_MD.strip() + "\n", encoding="utf-8")

print(f"Generación finalizada con éxito en: {DESTINO}")
