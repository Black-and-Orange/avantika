import React from 'react';

export function Divider({ tone = 'light', accent, width = '100%', style, ...rest }) {
  if (accent) {
    return <hr style={{ border: 'none', height: 2, width: 32, margin: 0, background: tone === 'inverse' ? 'var(--av-cyan)' : 'var(--av-magenta)', ...style }} {...rest} />;
  }
  return <hr style={{ border: 'none', height: 1, width, margin: 0, background: tone === 'inverse' ? 'var(--av-line-inverse)' : 'var(--av-line)', ...style }} {...rest} />;
}
