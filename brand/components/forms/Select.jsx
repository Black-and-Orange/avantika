import React from 'react';

export function Select({ label, options = [], style, id, ...rest }) {
  const selectId = id || React.useId();
  return (
    <div style={{ display: 'grid', gap: 'var(--av-space-1)', fontFamily: 'var(--av-font-text)', letterSpacing: 'var(--av-track-text)', color: 'var(--av-navy)', ...style }}>
      {label ? <label htmlFor={selectId} style={{ fontSize: '13px', fontWeight: 'var(--av-weight-semibold)' }}>{label}</label> : null}
      <select id={selectId} style={{
        width: '100%', boxSizing: 'border-box', height: 48, padding: '0 16px',
        fontFamily: 'inherit', fontWeight: 'var(--av-weight-regular)', fontSize: 'var(--av-size-body)', letterSpacing: 'inherit',
        color: 'var(--av-navy)', background: 'var(--av-blanco)',
        border: '1px solid var(--av-navy)', borderRadius: 'var(--av-radius-control)',
      }} {...rest}>
        {options.map((o) => <option key={o} value={o}>{o}</option>)}
      </select>
    </div>
  );
}
