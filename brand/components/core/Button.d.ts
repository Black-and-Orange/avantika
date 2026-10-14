import * as React from 'react';

/**
 * Control de acción de Avantika: navy sólido, radio mínimo, texto en altas y bajas.
 *
 * @startingPoint section="Core" subtitle="Botones de marca en sus cinco variantes" viewport="700x220"
 */
export interface ButtonProps extends React.HTMLAttributes<HTMLElement> {
  /** `inverse` e `inverseOutline` van sobre navy o púrpura. `ghost` es el link subrayado en magenta. */
  variant?: 'primary' | 'secondary' | 'ghost' | 'inverse' | 'inverseOutline';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
  disabled?: boolean;
  /** Renderiza un ancla en lugar de un botón. */
  href?: string;
  children?: React.ReactNode;
}
export function Button(props: ButtonProps): JSX.Element;
