import * as React from 'react';

/** Etiqueta corta: nombre de servicio o categoría. */
export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  /** `inverse` es cian sobre navy: el único lugar donde el cian funciona como texto. */
  tone?: 'outline' | 'navy' | 'purple' | 'inverse';
  children?: React.ReactNode;
}
export function Badge(props: BadgeProps): JSX.Element;
