// Carcasa de revisión: resalta la sección visible, alterna las zonas de Instagram y avisa del estado de las fuentes.
(function () {
  var enlaces = Array.prototype.slice.call(document.querySelectorAll('.rail__nav a'));
  var porId = {};
  enlaces.forEach(function (a) { porId[a.getAttribute('href').slice(1)] = a; });

  if ('IntersectionObserver' in window) {
    var observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (!entrada.isIntersecting) return;
        enlaces.forEach(function (a) { a.removeAttribute('aria-current'); });
        var enlace = porId[entrada.target.id];
        if (enlace) enlace.setAttribute('aria-current', 'true');
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    document.querySelectorAll('.bloque').forEach(function (seccion) { observador.observe(seccion); });
  }

  var menu = document.querySelector('.rail__nav details');
  var angosto = window.matchMedia('(max-width: 1039px)');
  function ajustarMenu() { if (menu) menu.open = !angosto.matches; }
  ajustarMenu();
  angosto.addEventListener('change', ajustarMenu);
  enlaces.forEach(function (a) {
    a.addEventListener('click', function () { if (menu && angosto.matches) menu.open = false; });
  });

  // Avisa si las fuentes de marca están instaladas en este equipo (no se distribuyen con la página).
  var aviso = document.getElementById('estado-fuentes');
  if (aviso && document.fonts && document.fonts.load) {
    var prueba = function (familia) {
      return document.fonts.load('700 16px "' + familia + '"').then(function (caras) { return caras.length > 0; }, function () { return false; });
    };
    Promise.all([prueba('Nebulica'), prueba('Swiza')]).then(function (r) {
      var linea = document.createElement('span');
      linea.style.display = 'block';
      linea.style.marginTop = '6px';
      linea.style.fontWeight = '600';
      linea.textContent = 'En este equipo: Nebulica ' + (r[0] ? 'instalada' : 'no instalada, ves el fallback') + ' · Swiza ' + (r[1] ? 'instalada' : 'no instalada, ves el fallback') + '.';
      aviso.appendChild(linea);
    });
  }

  var boton = document.getElementById('boton-ig');
  var lienzo = document.getElementById('lienzo-stories');
  if (boton && lienzo) {
    boton.addEventListener('click', function () {
      var activo = lienzo.classList.toggle('mostrar-ig');
      boton.setAttribute('aria-pressed', activo ? 'true' : 'false');
      boton.textContent = activo ? 'Ocultar lo que tapa la interfaz de Instagram' : 'Mostrar lo que tapa la interfaz de Instagram';
    });
  }
})();
