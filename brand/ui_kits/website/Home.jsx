function Home({ go }) {
  const { Button, Card, Badge, Divider } = NS;
  /* Los cuatro textos de servicio son literales de las piezas de LinkedIn del material (posts 1, 2, 6 y 12). */
  const servicios = [
    { title: 'Soporte TI', body: 'Mesa de ayuda, técnicos en sitio y en campo.', icon: '28' },
    { title: 'Ciberseguridad', body: 'Protegemos lo que importa para que tú sigas creciendo.', icon: '15' },
    { title: 'Infraestructura', body: 'Redes, servidores y cableado que no detienen tu operación.', icon: '32' },
    { title: 'IA segura', body: 'Protegemos tus datos para que adoptes IA sin frenar tu operación.', icon: '14' },
  ];
  const datos = ['Disponibilidad', 'Tiempo de respuesta', 'Cobertura', 'Años de operación'];
  return (
    <main>
      <div style={{ height: 'clamp(180px, 28vw, 360px)', overflow: 'hidden', background: 'var(--av-navy)' }}>
        <img src="../../assets/imagery-layout-12.jpg" alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      </div>
      <div style={{ background: 'var(--av-navy)', color: 'var(--av-hielo)' }}>
        <div className="shell" style={{ paddingTop: 'var(--av-space-5)', paddingBottom: 'var(--av-space-5)', display: 'grid', gap: 'var(--av-space-3)', justifyItems: 'start' }}>
          <Badge tone="inverse">Cybersecurity</Badge>
          <h1 style={{ fontSize: 'var(--av-size-display)', maxWidth: '20ch' }}>Un solo equipo ordena, protege y monitorea tu TI</h1>
          <p style={{ margin: 0, maxWidth: '56ch', fontSize: '18px', fontWeight: 300 }}>Tu tecnología al ritmo de tu operación.</p>
          <div style={{ display: 'flex', gap: 'var(--av-space-2)', flexWrap: 'wrap' }}>
            <Button variant="inverse" onClick={() => go('contacto')}>Agenda tu diagnóstico</Button>
            <Button variant="inverseOutline" onClick={() => go('contacto')}>Habla con un especialista</Button>
          </div>
        </div>
      </div>

      <section>
        <div className="shell" style={{ display: 'grid', gap: 'var(--av-space-4)' }}>
          <div style={{ display: 'grid', gap: 'var(--av-space-1)' }}>
            <Divider accent />
            <span className="eyebrow">Servicios</span>
            <h2>Ordena, protege, crece</h2>
          </div>
          <div style={{ display: 'grid', gap: 'var(--av-space-3)', gridTemplateColumns: 'repeat(auto-fit, minmax(230px, 1fr))' }}>
            {servicios.map((s) => (
              <Card key={s.title} title={s.title}
                    eyebrow={<img src={'../../assets/icons/avantika-icono-' + s.icon + '.png'} alt="" style={{ width: 64, height: 64, marginBottom: 8 }} />}>
                {s.body}
              </Card>
            ))}
          </div>
        </div>
      </section>

      <section style={{ paddingTop: 0 }}>
        <div className="shell" style={{ display: 'grid', gap: 'var(--av-space-4)', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', alignItems: 'center' }}>
          <img src="../../assets/imagery-foto-soc-you-can.jpg" alt="Centro de monitoreo de Avantika" style={{ width: '100%', aspectRatio: '3 / 2', objectFit: 'cover' }} />
          <div style={{ display: 'grid', gap: 'var(--av-space-2)' }}>
            <span className="eyebrow">Nosotros</span>
            <h2>Un solo equipo</h2>
            {/* Visión de la empresa, transcrita del muro de su oficina (foto oficina-vision). */}
            <p style={{ margin: 0 }}>Nuestra visión es ser la compañía de Ciberseguridad &amp; TI preferida en México por su confiabilidad, participación de mercado y ecosistema único de formación de especialistas.</p>
          </div>
        </div>
      </section>

      <section style={{ paddingTop: 0 }}>
        <div className="shell" style={{ display: 'grid', gap: 'var(--av-space-4)', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', alignItems: 'start' }}>
          <div style={{ display: 'grid', gap: 'var(--av-space-2)' }}>
            <span className="eyebrow">En cifras</span>
            <h2>Datos por validar</h2>
            <p style={{ margin: 0 }}>Las piezas de LinkedIn mencionan «Disponibilidad 99%», «Monitoreo 24/7», «SLA cumplido» y cobertura «en todo México». Ninguna cifra tiene respaldo en el material, así que aquí van como placeholder.</p>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 1, background: 'var(--av-line)', border: 'var(--av-border-hairline)' }}>
            {datos.map((d) => (
              <div key={d} style={{ background: 'var(--av-hielo)', padding: 'var(--av-space-3)', display: 'grid', gap: 'var(--av-space-1)', minWidth: 0 }}>
                <span><Ph /></span><span style={{ fontSize: '13px' }}>{d}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <div style={{ background: 'var(--av-purple)', color: 'var(--av-hielo)', textAlign: 'center' }}>
        <div className="shell" style={{ paddingTop: 'var(--av-space-6)', paddingBottom: 'var(--av-space-6)', display: 'grid', gap: 'var(--av-space-3)', justifyItems: 'center' }}>
          <h2 style={{ color: 'var(--av-hielo)' }}>Hoy, tu empresa no se detiene</h2>
          <p style={{ margin: 0 }}>Tú sigue creciendo. Nosotros cuidamos tu espalda.</p>
          <Button variant="inverse" onClick={() => go('contacto')}>Agenda tu diagnóstico</Button>
        </div>
      </div>
    </main>
  );
}
