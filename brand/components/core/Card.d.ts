import * as React from 'react';

/** Tarjeta de servicio o de paso: filete de 1 px, sin sombra ni redondeo. */
export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Ruta de imagen. Usa los fondos entregados (`assets/imagery-layout-*`); no hay fotografía de marca. */
  media?: string;
  mediaAlt?: string;
  /** Texto corto o un nodo (por ejemplo, un ícono del set). */
  eyebrow?: React.ReactNode;
  title?: string;
  footer?: React.ReactNode;
  tone?: 'light' | 'hielo' | 'navy';
  children?: React.ReactNode;
}
export function Card(props: CardProps): JSX.Element;
