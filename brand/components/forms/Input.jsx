import React from 'react';

export function Input({ label, hint, style, id, ...rest }) {
  const [focus, setFocus] = React.useState(false);
  const inputId = id || React.useId();
  return (
    <div style={{ display: 'grid', gap: 'var(--av-space-1)', fontFamily: 'var(--av-font-text)', letterSpacing: 'var(--av-track-text)', color: 'var(--av-navy)', ...style }}>
      {label ? <label htmlFor={inputId} style={{ fontSize: '13px', fontWeight: 'var(--av-weight-semibold)' }}>{label}</label> : null}
      <input id={inputId} style={{
        width: '100%', boxSizing: 'border-box', height: 48, padding: '0 16px',
        fontFamily: 'inherit', fontWeight: 'var(--av-weight-regular)', fontSize: 'var(--av-size-body)', letterSpacing: 'inherit',
        color: 'var(--av-navy)', background: 'var(--av-blanco)',
        border: '1px solid var(--av-navy)', borderRadius: 'var(--av-radius-control)',
        outline: focus ? '2px solid var(--av-magenta)' : 'none', outlineOffset: 2,
      }} onFocus={() => setFocus(true)} onBlur={() => setFocus(false)} {...rest} />
      {hint ? <div style={{ fontSize: '13px', fontWeight: 'var(--av-weight-regular)' }}>{hint}</div> : null}
    </div>
  );
}
