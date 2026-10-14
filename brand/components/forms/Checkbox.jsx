import React from 'react';

export function Checkbox({ children, style, id, ...rest }) {
  const checkId = id || React.useId();
  return (
    <label htmlFor={checkId} style={{ display: 'flex', gap: 'var(--av-space-1)', alignItems: 'center', fontFamily: 'var(--av-font-text)', fontWeight: 'var(--av-weight-regular)', letterSpacing: 'var(--av-track-text)', fontSize: 'var(--av-size-small)', color: 'var(--av-navy)', ...style }}>
      <input id={checkId} type="checkbox" style={{ width: 16, height: 16, accentColor: 'var(--av-navy)', margin: 0 }} {...rest} />
      <span>{children}</span>
    </label>
  );
}
