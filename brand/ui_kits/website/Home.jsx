function Home({ go }) {
  const { Button, Badge, Divider } = NS;
  /* Textos de servicio y de la historia: literales de las piezas de LinkedIn del material.
     Visión: transcrita del muro de la oficina (foto oficina-vision). Rótulos de los pasos: BnO. */
  const servicios = [
    { title: 'Soporte TI', body: 'Mesa de ayuda, técnicos en sitio y en campo.', icon: '28' },
    { title: 'Ciberseguridad', body: 'Protegemos lo que importa para que tú sigas creciendo.', icon: '15' },
    { title: 'Infraestructura', body: 'Redes, servidores y cableado que no detienen tu operación.', icon: '32' },
    { title: 'IA segura', body: 'Protegemos tus datos para que adoptes IA sin frenar tu operación.', icon: '14' },
  ];
  const pasos = [
    ['01 · El problema', 'Lunes, 9 am. El sistema cayó. Nadie responde.', 'Ventas detenidas. Clientes esperando. Y tú, sin saber a quién llamar.'],
    ['02 · Lo que pasó', 'Nadie falló. Creciste.', 'Tu empresa avanzó más rápido que tu tecnología.'],
    ['03 · Lo que cambia', 'Hoy, tu empresa no se detiene.', 'Un solo equipo ordena, protege y monitorea tu TI.'],
  ];
  const cifras = ['Disponibilidad', 'Tiempo de respuesta', 'Cobertura', 'Horario de monitoreo'];
  return (
    <main>
      <section className="dark" style={{ padding: 0 }}>
        <div className="shell lp-hero">
          <div style={{ display: 'grid', gap: 'var(--av-space-3)', justifyItems: 'start' }}>
            <Badge tone="inverse">Cybersecurity</Badge>
            <h1 style={{ fontSize: 'clamp(36px, 4.6vw, 60px)', lineHeight: 1.05 }}>Un solo equipo ordena, protege y monitorea tu TI</h1>
            <p style={{ margin: 0, maxWidth: '40ch', fontSize: '18px', fontWeight: 300 }}>Tu tecnología al ritmo de tu operación.</p>
            <div style={{ display: 'flex', gap: 'var(--av-space-2)', flexWrap: 'wrap' }}>
              <Button variant="inverse" onClick={() => go('contacto')}>Agenda tu diagnóstico</Button>
              <Button variant="inverseOutline" onClick={() => go('contacto')}>Habla con un especialista</Button>
            </div>
            <ul className="lp-temas">{servicios.map((s) => <li key={s.title}>{s.title}</li>)}</ul>
          </div>
          <figure className="lp-foto">
            <img src="../../assets/imagery-foto-soc-you-can.jpg" alt="Centro de monitoreo de Avantika" />
            <figcaption>Centro de monitoreo Avantika</figcaption>
          </figure>
        </div>
      </section>

      <section>
        <div className="shell">
          <div style={{ display: 'grid', gap: 'var(--av-space-1)', justifyItems: 'start', marginBottom: 'var(--av-space-4)' }}>
            <Divider accent />
            <span className="eyebrow">Servicios</span>
            <h2>Ordena, protege, crece</h2>
          </div>
          <div>
            {servicios.map((s, i) => (
              <div key={s.title} className="lp-fila">
                <span className="lp-num">{String(i + 1).padStart(2, '0')}</span>
                <h3 style={{ fontSize: '22px' }}>{s.title}</h3>
                <p style={{ margin: 0, fontSize: '15px' }}>{s.body}</p>
                <img src={'../../assets/icons/avantika-icono-' + s.icon + '.png'} alt="" style={{ width: 56, height: 56 }} />
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="tinta lp-historia" style={{ padding: 0 }}>
        <img src="../../assets/imagery-foto-detalle-teclado-1.jpg" alt="Manos de un especialista sobre el teclado" />
        <div style={{ padding: 'var(--av-space-6) var(--av-space-5)', display: 'grid', gap: 'var(--av-space-4)', alignContent: 'center' }}>
          {pasos.map(([etiqueta, titular, apoyo]) => (
            <div key={etiqueta} className="lp-paso">
              <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--av-cyan)' }}>{etiqueta}</span>
              <h3 style={{ fontSize: 'clamp(20px, 2.2vw, 28px)' }}>{titular}</h3>
              <p style={{ margin: 0, fontSize: '15px', fontWeight: 300 }}>{apoyo}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="dark">
        <div className="shell">
          <div style={{ display: 'grid', gap: 'var(--av-space-1)', justifyItems: 'start', marginBottom: 'var(--av-space-4)' }}>
            <Divider accent tone="inverse" />
            <span className="eyebrow" style={{ color: 'var(--av-cyan)' }}>Nosotros</span>
            <h2>Un solo equipo</h2>
          </div>
          <blockquote style={{ margin: '0 0 var(--av-space-5)', maxWidth: '34ch', fontSize: 'clamp(20px, 2.2vw, 28px)', fontWeight: 300, lineHeight: 1.35 }}>
            Nuestra visión es ser la compañía de Ciberseguridad &amp; TI preferida en México por su confiabilidad, participación de mercado y ecosistema único de formación de especialistas.
          </blockquote>
          <div className="lp-retratos">
            {[1, 2, 3].map((n) => <img key={n} src={'../../assets/imagery-foto-retrato-oscuro-0' + n + '.jpg'} alt="Retrato de una persona del equipo de Avantika" />)}
          </div>
          <div className="lp-cifras">
            {cifras.map((c) => <div key={c}><span>{c}</span><Ph inverse /></div>)}
          </div>
        </div>
      </section>

      <section style={{ background: 'var(--av-purple)', color: 'var(--av-hielo)', padding: 'var(--av-space-6) 0' }}>
        <div className="shell" style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--av-space-3) var(--av-space-5)', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'grid', gap: 'var(--av-space-2)', maxWidth: '46ch' }}>
            <h2 style={{ color: 'var(--av-hielo)' }}>Tú sigue corriendo. Nosotros cuidamos tu espalda.</h2>
            <p style={{ margin: 0 }}>Agenda un diagnóstico de tu soporte, tu seguridad y tu infraestructura.</p>
          </div>
          <Button variant="inverse" onClick={() => go('contacto')}>Agenda tu diagnóstico</Button>
        </div>
      </section>
    </main>
  );
}
