import * as React from 'react';

/** Filete de 1 px, o pleca de acento de 32 × 2 px con `accent` (magenta sobre claro, cian sobre navy). */
export interface DividerProps extends React.HTMLAttributes<HTMLHRElement> {
  tone?: 'light' | 'inverse';
  accent?: boolean;
  width?: string | number;
}
export function Divider(props: DividerProps): JSX.Element;
