/* ds-runtime.js — shim de desarrollo.
   El compilador del design system entrega un _ds_bundle.js generado que expone todos los
   componentes bajo un solo namespace global. Mientras ese bundle no exista, este shim descarga
   las fuentes de los componentes, les quita la sintaxis ESM, las evalúa con Babel y expone la
   misma forma. Nada de esto es API pública del sistema. Necesita servirse por http (usa fetch). */
(function () {
  var FILES = [
    'components/core/Button.jsx',
    'components/core/Badge.jsx',
    'components/core/Card.jsx',
    'components/core/Divider.jsx',
    'components/forms/Input.jsx',
    'components/forms/Select.jsx',
    'components/forms/Checkbox.jsx'
  ];

  function findCompiled() {
    for (var k in window) {
      try {
        var v = window[k];
        if (v && typeof v === 'object' && v.Button && v.Card && v.Input) return v;
      } catch (e) {}
    }
    return null;
  }

  var root = document.currentScript.getAttribute('data-root') || '.';

  function loadBundle() {
    return fetch(root + '/_ds_bundle.js').then(function (r) {
      if (!r.ok) return null;
      return r.text().then(function (code) {
        var tag = document.createElement('script');
        tag.textContent = code;
        document.head.appendChild(tag);
        return findCompiled();
      });
    }).catch(function () { return null; });
  }

  window.__dsReady = loadBundle().then(function (bundled) {
    if (bundled) return bundled;
    return fallback();
  });

  function fallback() { return new Promise(function (resolve) {
    var compiled = findCompiled();
    if (compiled) return resolve(compiled);
    var ns = {};
    Promise.all(FILES.map(function (rel) {
      return fetch(root + '/' + rel).then(function (r) { return r.ok ? r.text() : ''; }).catch(function () { return ''; });
    })).then(function (sources) {
      sources.forEach(function (src, i) {
        if (!src) return;
        var code = src
          .replace(/^[ \t]*import[\s\S]*?;[ \t]*$/gm, '')
          .replace(/^[ \t]*export[ \t]+/gm, '');
        var names = [];
        src.replace(/export\s+function\s+([A-Za-z0-9_]+)/g, function (_, n) { names.push(n); return _; });
        try {
          var out = Babel.transform(code, { presets: [['react', { runtime: 'classic' }]], sourceType: 'script' }).code;
          var fn = new Function('React', 'exports', out + '\n' + names.map(function (n) { return 'exports.' + n + ' = ' + n + ';'; }).join('\n'));
          fn(window.React, ns);
        } catch (e) {
          console.error('ds-runtime: failed on ' + FILES[i] + ' :: ' + (e && (e.message || e.toString())));
        }
      });
      resolve(ns);
    });
  }); }
})();
