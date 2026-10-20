const NAV = [
  { key: 'home', label: 'Servicios' },
  { key: 'contacto', label: 'Contacto' },
];

function SiteHeader({ route, go }) {
  const { Button } = NS;
  return (
    <header style={{ position: 'sticky', top: 0, zIndex: 50, background: 'var(--av-navy)', borderBottom: 'var(--av-border-inverse)' }}>
      <div className="shell" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 'var(--av-space-3)', minHeight: 72, paddingTop: 8, paddingBottom: 8 }}>
        <button onClick={() => go('home')} aria-label="Avantika, inicio" style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}>
          <img src="../revision/img/logos/logo-avantika-blanco.png" alt="Avantika" style={{ height: 18, width: 'auto' }} />
        </button>
        <nav style={{ display: 'flex', alignItems: 'center', gap: 'var(--av-space-3)' }}>
          <span className="lp-nav-links" style={{ display: 'flex', gap: 'var(--av-space-3)' }}>
            {NAV.map((n) => (
              <button key={n.key} onClick={() => go(n.key)} style={{
                background: 'none', border: 'none', cursor: 'pointer', padding: '4px 0',
                fontFamily: 'var(--av-font-text)', fontSize: 'var(--av-size-small)', letterSpacing: 'var(--av-track-text)',
                fontWeight: route === n.key ? 'var(--av-weight-semibold)' : 'var(--av-weight-regular)',
                color: 'var(--av-hielo)', borderBottom: '2px solid ' + (route === n.key ? 'var(--av-cyan)' : 'transparent'),
              }}>{n.label}</button>
            ))}
          </span>
          <Button size="sm" variant="inverse" onClick={() => go('contacto')}>Agenda tu diagnóstico</Button>
        </nav>
      </div>
    </header>
  );
}

function SiteFooter() {
  return (
    <footer className="tinta">
      <div className="shell" style={{ paddingTop: 'var(--av-space-5)', paddingBottom: 'var(--av-space-5)', display: 'grid', gap: 'var(--av-space-4)', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', alignItems: 'start', fontSize: '13px' }}>
        <img src="../revision/img/logos/logo-avantika-tagline-blanco-azul.png" alt="Avantika Cybersecurity" style={{ width: 200 }} />
        <div><b style={{ fontWeight: 600 }}>Contacto</b><br /><Ph inverse /><br /><Ph inverse /></div>
        <div><b style={{ fontWeight: 600 }}>Sitio</b><br />avantika.mx</div>
        <p style={{ gridColumn: '1 / -1', margin: 0, borderTop: 'var(--av-border-inverse)', paddingTop: 'var(--av-space-2)', fontSize: '12px' }}>
          Sitio de muestra armado por Black &amp; Orange. Los textos son propuesta o vienen de las piezas de LinkedIn y del muro de la oficina; ningún dato está validado.
        </p>
      </div>
    </footer>
  );
}

/* Placeholder visible para todo dato sin respaldo del cliente. */
function Ph({ inverse }) {
  return <span style={{
    background: inverse ? 'rgba(244,250,255,.10)' : 'rgba(135,0,125,.10)',
    outline: '1px dashed ' + (inverse ? 'var(--av-hielo)' : 'var(--av-purple)'),
    padding: '0 4px', fontFamily: 'var(--av-font-text)', fontWeight: 400, fontSize: '14px', letterSpacing: 'var(--av-track-text)', textTransform: 'none',
  }}>[Dato por validar]</span>;
}
