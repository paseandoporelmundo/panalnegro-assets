/**
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
