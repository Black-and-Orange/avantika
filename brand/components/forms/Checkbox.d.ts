import * as React from 'react';

/** Casilla nativa teñida de navy. */
export interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
  children?: React.ReactNode;
}
export function Checkbox(props: CheckboxProps): JSX.Element;
