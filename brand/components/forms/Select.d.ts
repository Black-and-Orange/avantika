import * as React from 'react';

/** Lista desplegable nativa con la misma caja que `Input`. */
export interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options?: string[];
}
export function Select(props: SelectProps): JSX.Element;
