import React from 'react';

const base = {
  fontFamily: 'var(--av-font-text)',
  fontWeight: 'var(--av-weight-semibold)',
  letterSpacing: 'var(--av-track-text)',
  lineHeight: 1,
  border: '1px solid transparent',
  borderRadius: 'var(--av-radius-control)',
  cursor: 'pointer',
  display: 'inline-flex',
  alignItems: 'center',
  justifyContent: 'center',
  gap: 'var(--av-space-1)',
  textDecoration: 'none',
  boxSizing: 'border-box',
  transition: 'background 160ms ease, color 160ms ease, border-color 160ms ease',
};

const sizes = {
  sm: { fontSize: '13px', minHeight: 40, padding: '8px 16px' },
  md: { fontSize: '14px', minHeight: 48, padding: '8px 24px' },
  lg: { fontSize: '16px', minHeight: 56, padding: '8px 32px' },
};

const variants = {
  primary: { background: 'var(--av-navy)', color: 'var(--av-hielo)', borderColor: 'var(--av-navy)' },
  secondary: { background: 'transparent', color: 'var(--av-navy)', borderColor: 'var(--av-navy)' },
  ghost: { background: 'transparent', color: 'var(--av-navy)', borderColor: 'transparent', padding: '8px 0', textDecoration: 'underline', textDecorationColor: 'var(--av-magenta)', textDecorationThickness: '2px', textUnderlineOffset: '6px' },
  inverse: { background: 'var(--av-hielo)', color: 'var(--av-navy)', borderColor: 'var(--av-hielo)' },
  inverseOutline: { background: 'transparent', color: 'var(--av-hielo)', borderColor: 'var(--av-hielo)' },
};

const hovers = {
  primary: { background: 'var(--av-navy-hover)', borderColor: 'var(--av-navy-hover)' },
  secondary: { background: 'var(--av-navy)', color: 'var(--av-hielo)' },
  ghost: { color: 'var(--av-purple)' },
  inverse: { background: 'var(--av-blanco)', borderColor: 'var(--av-blanco)' },
  inverseOutline: { background: 'var(--av-hielo)', color: 'var(--av-navy)' },
};

export function Button({ variant = 'primary', size = 'md', fullWidth, disabled, href, children, style, onClick, ...rest }) {
  const [hover, setHover] = React.useState(false);
  const Tag = href ? 'a' : 'button';
  const s = {
    ...base,
    ...sizes[size],
    ...variants[variant],
    ...(hover && !disabled ? hovers[variant] : null),
    ...(fullWidth ? { width: '100%' } : null),
    ...(disabled ? { opacity: 0.45, cursor: 'not-allowed' } : null),
    ...style,
  };
  return (
    <Tag
      href={href}
      style={s}
      disabled={!href ? disabled : undefined}
      onClick={disabled ? undefined : onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      {...rest}
    >
      {children}
    </Tag>
  );
}
