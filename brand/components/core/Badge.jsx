import React from 'react';

export function Badge({ tone = 'outline', children, style, ...rest }) {
  const tones = {
    outline: { background: 'transparent', color: 'var(--av-navy)', borderColor: 'var(--av-navy)' },
    navy: { background: 'var(--av-navy)', color: 'var(--av-hielo)', borderColor: 'var(--av-navy)' },
    purple: { background: 'var(--av-purple)', color: 'var(--av-hielo)', borderColor: 'var(--av-purple)' },
    inverse: { background: 'transparent', color: 'var(--av-cyan)', borderColor: 'var(--av-cyan)' },
  }[tone];
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center',
      fontFamily: 'var(--av-font-text)', fontSize: '12px', fontWeight: 'var(--av-weight-semibold)',
      letterSpacing: 'var(--av-track-text)', lineHeight: 1,
      padding: '8px 16px', border: '1px solid', borderRadius: 'var(--av-radius-card)', ...tones, ...style,
    }} {...rest}>{children}</span>
  );
}
