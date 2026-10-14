function Contact() {
  const { Button, Input, Select, Checkbox } = NS;
  const [sent, setSent] = React.useState(false);
  return (
    <main>
      <section>
        <div className="shell" style={{ display: 'grid', gap: 'var(--av-space-5)', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', alignItems: 'start' }}>
          <div style={{ display: 'grid', gap: 'var(--av-space-2)' }}>
            <span className="eyebrow">Contacto</span>
            <h1 style={{ fontSize: 'var(--av-size-h1)' }}>Agenda tu diagnóstico</h1>
            <p style={{ margin: 0 }}>Déjanos tus datos y un especialista te contactará para revisar tu soporte, tu seguridad y tu infraestructura.</p>
            <p style={{ margin: 0, fontSize: '13px' }}>Formulario de muestra: no envía datos. Una pieza de LinkedIn ofrece el diagnóstico «sin costo»; esa condición está por validar y aquí no se promete.</p>
          </div>
          <form onSubmit={(e) => { e.preventDefault(); setSent(true); }} style={{ display: 'grid', gap: 'var(--av-space-3)', background: 'var(--av-blanco)', border: 'var(--av-border-hairline)', padding: 'var(--av-space-4)' }}>
            <Input label="Nombre completo" />
            <Input label="Correo de trabajo" placeholder="nombre@empresa.com" />
            <Input label="Teléfono" hint="Con lada" />
            <Select label="Me interesa" options={['Soporte TI', 'Ciberseguridad', 'Infraestructura', 'IA segura']} />
            <Checkbox>Acepto el aviso de privacidad</Checkbox>
            <Button disabled={sent}>{sent ? 'Enviado' : 'Enviar'}</Button>
          </form>
        </div>
      </section>
    </main>
  );
}
