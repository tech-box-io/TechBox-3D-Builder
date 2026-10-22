// Only TechBox's LMS may show a guide inside a frame: the server's Content-Security-Policy frame-ancestors is the real check,
// this is a second guard (made by tools/site_pages.py from guides.json embed_origins; every published guide loads it).
(function () {
  if (window.top === window.self) return;
  var allowed = ["https://edu.tech-box.io", "https://techbox-front.vercel.app"], bad = false, ao = location.ancestorOrigins;
  var local = function (o) { return /^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(o); };
  if (ao && ao.length) {
    for (var i = 0; i < ao.length; i++) if (ao[i] !== 'null' && allowed.indexOf(ao[i]) < 0 && !local(ao[i])) bad = true;
  } else if (document.referrer) {
    try { var o = new URL(document.referrer).origin; if (o !== location.origin && allowed.indexOf(o) < 0 && !local(o)) bad = true; } catch (e) {}
  }
  if (!bad) return;
  window.techboxFrameRefused = true;
  document.documentElement.style.visibility = 'hidden';
  document.addEventListener('DOMContentLoaded', function () {
    var p = document.createElement('p'), a = document.createElement('a');
    a.href = location.href; a.target = '_blank'; a.rel = 'noopener'; a.textContent = 'Open this build guide in a new tab';
    p.style.cssText = 'font:16px system-ui,sans-serif;padding:16px'; p.appendChild(a);
    document.body.replaceChildren(p); document.documentElement.style.visibility = '';
  });
})();
