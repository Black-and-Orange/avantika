# UI kit — Sitio de captación Avantika

Aplicación original de la identidad de Avantika a un sitio de captación. No se entregó sitio, Figma ni
código (el material solo menciona el dominio `avantika.mx`, que no se revisó), así que esto es una
propuesta de BnO y no la recreación de un producto existente.

**Pantallas**

| Archivo | Pantalla | Notas |
| --- | --- | --- |
| `Chrome.jsx` | `SiteHeader`, `SiteFooter`, `Ph` | Encabezado claro con logotipo negro; pie navy con logotipo y tagline en cian. `Ph` es el placeholder de dato sin validar. |
| `Home.jsx` | Home | Fondo de marca arriba y banda navy con el titular (el texto no va sobre la imagen), cuatro servicios con íconos del set, «Nosotros» con la foto del centro de monitoreo y la visión de la empresa, cifras como placeholder y banda de cierre púrpura. |
| `Contact.jsx` | Contacto | Formulario de muestra. No envía datos. |

`index.html` las une con ruteo en memoria y carga los componentes con `ds-runtime.js`, así que cada
pantalla se compone con las primitivas del sistema. Necesita servirse por http (no abre con doble clic)
y conexión a internet para React y Babel (unpkg).

Los titulares y los textos de servicio son literales de las piezas de LinkedIn del material; no consta
que el cliente los haya aprobado. La visión de «Nosotros» está transcrita del muro de la oficina, que se ve
en la sesión de fotos. La foto muestra a personas del equipo: falta su autorización de uso de imagen. Toda cifra va como `[Dato por validar]`.

Las tipografías Nebulica y Swiza no se distribuyen con el repo (licencia): se ven solo si están
instaladas en el equipo. Si no, aparece el fallback del sistema.

`../revision/` es la página de revisión del sistema completo (la que se publica en GitHub Pages).
