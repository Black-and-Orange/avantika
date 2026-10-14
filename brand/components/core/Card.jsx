import React from 'react';

export function Card({ media, mediaAlt = '', eyebrow, title, children, footer, tone = 'light', style, ...rest }) {
  const inverse = tone === 'navy';
  const tones = {
    light: { background: 'var(--av-blanco)', color: 'var(--av-navy)', border: 'var(--av-border-hairline)' },
    hielo: { background: 'var(--av-hielo)', color: 'var(--av-navy)', border: 'var(--av-border-hairline)' },
    navy: { background: 'var(--av-navy)', color: 'var(--av-hielo)', border: '1px solid var(--av-navy)' },
  }[tone];
  return (
    <div
      style={{
        display: 'flex', flexDirection: 'column',
        borderRadius: 'var(--av-radius-card)', overflow: 'hidden',
        fontFamily: 'var(--av-font-text)', fontWeight: 'var(--av-weight-regular)', letterSpacing: 'var(--av-track-text)',
        ...tones, ...style,
      }}
      {...rest}
    >
      {media ? <img src={media} alt={mediaAlt} style={{ display: 'block', width: '100%', aspectRatio: '16 / 9', objectFit: 'cover' }} /> : null}
      <div style={{ padding: 'var(--av-space-3)', display: 'flex', flexDirection: 'column', gap: 'var(--av-space-1)', flex: 1, alignItems: 'flex-start' }}>
        {eyebrow ? (
          <span style={{ fontSize: 'var(--av-size-caption)', fontWeight: 'var(--av-weight-semibold)', color: inverse ? 'var(--av-cyan)' : 'var(--av-purple)' }}>{eyebrow}</span>
        ) : null}
        {title ? (
          <h3 style={{
            margin: 0, fontFamily: 'var(--av-font-display)', fontWeight: 'var(--av-weight-semibold)',
            letterSpacing: 'var(--av-track-title)', fontSize: '20px', lineHeight: 'var(--av-lh-title)',
          }}>{title}</h3>
        ) : null}
        {children ? <div style={{ fontSize: 'var(--av-size-small)', lineHeight: 'var(--av-lh-text)' }}>{children}</div> : null}
        {footer ? <div style={{ marginTop: 'auto', paddingTop: 'var(--av-space-2)' }}>{footer}</div> : null}
      </div>
    </div>
  );
}
