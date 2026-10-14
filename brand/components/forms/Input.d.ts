import * as React from 'react';

/** Campo de texto con etiqueta arriba: borde navy fino sobre blanco, foco magenta. */
export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  hint?: string;
}
export function Input(props: InputProps): JSX.Element;
