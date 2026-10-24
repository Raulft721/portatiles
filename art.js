/* =========================================================
   Ilustraciones vectoriales de portátiles
   ---------------------------------------------------------
   Sustituyen a las fotos de stock. Son dibujos genéricos:
   NO representan el modelo real, solo su tipo de equipo.
   Uso:  laptopArt(laptop, "id-unico")
   ========================================================= */
(function (global) {
  "use strict";

  var FALLBACK = ["#0071e3", "#67c1ff"];

  function palette(hex) {
    var found = String(hex || "").match(/#[0-9a-fA-F]{6}/g) || [];
    return [found[0] || FALLBACK[0], found[1] || found[0] || FALLBACK[1]];
  }

  function kindOf(l) {
    if (l.scores && l.scores.gaming >= 78) return "gaming";
    if (l.os === "ChromeOS") return "chromebook";
    if (l.weight <= 1.25) return "ultra";
    if (l.scores && l.scores.trabajo >= 86) return "work";
    return "study";
  }

  function content(kind, c2) {
    if (kind === "gaming") {
      return '<circle cx="198" cy="82" r="34" fill="' + c2 + '" opacity=".09"/>'
        + '<circle cx="198" cy="82" r="17" fill="none" stroke="' + c2 + '" stroke-opacity=".5" stroke-width="2"/>'
        + '<circle cx="198" cy="82" r="2.5" fill="' + c2 + '"/>'
        + '<path d="M198 62v-5M198 102v5M178 82h-5M218 82h5" stroke="' + c2 + '" stroke-opacity=".45" stroke-width="2" stroke-linecap="round"/>'
        + '<rect x="82" y="54" width="38" height="5" rx="2.5" fill="#e2e8f0" opacity=".75"/>'
        + '<rect x="82" y="65" width="24" height="4" rx="2" fill="#e2e8f0" opacity=".35"/>'
        + '<rect x="82" y="104" width="16" height="8" rx="2" fill="' + c2 + '" opacity=".5"/>'
        + '<rect x="102" y="104" width="16" height="8" rx="2" fill="' + c2 + '" opacity=".3"/>'
        + '<rect x="176" y="114" width="58" height="9" rx="3" fill="' + c2 + '" opacity=".3"/>'
        + '<rect x="176" y="114" width="34" height="9" rx="3" fill="' + c2 + '" opacity=".7"/>';
    }

    if (kind === "chromebook") {
      return '<rect x="76" y="47" width="168" height="12" rx="3" fill="#ffffff" opacity=".06"/>'
        + '<circle cx="85" cy="53" r="2.4" fill="#f87171"/>'
        + '<circle cx="93" cy="53" r="2.4" fill="#fbbf24"/>'
        + '<circle cx="101" cy="53" r="2.4" fill="#34d399"/>'
        + '<rect x="110" y="49" width="46" height="8" rx="2" fill="#ffffff" opacity=".12"/>'
        + '<rect x="82" y="66" width="80" height="62" rx="4" fill="#ffffff" opacity=".09"/>'
        + '<rect x="170" y="66" width="64" height="28" rx="4" fill="' + c2 + '" opacity=".35"/>'
        + '<rect x="170" y="100" width="64" height="28" rx="4" fill="' + c2 + '" opacity=".16"/>';
    }

    if (kind === "ultra") {
      return '<rect x="82" y="56" width="104" height="7" rx="3.5" fill="' + c2 + '" opacity=".85"/>'
        + '<rect x="82" y="72" width="82" height="5" rx="2.5" fill="#e2e8f0" opacity=".45"/>'
        + '<rect x="82" y="83" width="60" height="5" rx="2.5" fill="#e2e8f0" opacity=".3"/>'
        + '<rect x="82" y="94" width="70" height="5" rx="2.5" fill="#e2e8f0" opacity=".22"/>'
        + '<circle cx="206" cy="78" r="14" fill="' + c2 + '" opacity=".18"/>'
        + '<circle cx="206" cy="78" r="5" fill="' + c2 + '" opacity=".7"/>';
    }

    if (kind === "work") {
      return '<rect x="82" y="104" width="16" height="26" rx="3" fill="' + c2 + '" opacity=".5"/>'
        + '<rect x="104" y="88" width="16" height="42" rx="3" fill="' + c2 + '" opacity=".7"/>'
        + '<rect x="126" y="96" width="16" height="34" rx="3" fill="' + c2 + '" opacity=".4"/>'
        + '<rect x="148" y="74" width="16" height="56" rx="3" fill="' + c2 + '" opacity=".9"/>'
        + '<rect x="78" y="132" width="90" height="2" rx="1" fill="#94a3b8" opacity=".35"/>'
        + '<rect x="176" y="54" width="58" height="34" rx="4" fill="#ffffff" opacity=".07"/>'
        + '<rect x="184" y="62" width="28" height="4" rx="2" fill="#e2e8f0" opacity=".5"/>'
        + '<rect x="176" y="96" width="58" height="34" rx="4" fill="' + c2 + '" opacity=".14"/>'
        + '<rect x="184" y="104" width="34" height="4" rx="2" fill="' + c2 + '" opacity=".8"/>';
    }

    /* study */
    return '<rect x="82" y="54" width="38" height="6" rx="3" fill="' + c2 + '" opacity=".85"/>'
      + '<rect x="82" y="70" width="84" height="5" rx="2.5" fill="#e2e8f0" opacity=".5"/>'
      + '<rect x="82" y="81" width="70" height="5" rx="2.5" fill="#e2e8f0" opacity=".36"/>'
      + '<rect x="82" y="92" width="92" height="5" rx="2.5" fill="#e2e8f0" opacity=".28"/>'
      + '<rect x="82" y="103" width="48" height="5" rx="2.5" fill="#e2e8f0" opacity=".2"/>'
      + '<rect x="176" y="54" width="58" height="54" rx="5" fill="#ffffff" opacity=".06"/>'
      + '<rect x="184" y="62" width="38" height="4" rx="2" fill="#e2e8f0" opacity=".45"/>'
      + '<rect x="184" y="72" width="26" height="4" rx="2" fill="#e2e8f0" opacity=".3"/>';
  }

  function art(kind, c1, c2, uid) {
    var u = String(uid || "art").replace(/[^a-zA-Z0-9_-]/g, "") || "art";
    var baseY = kind === "gaming" ? 146 : 148;
    var baseH = kind === "gaming" ? 19 : kind === "ultra" ? 10 : 15;
    var baseR = kind === "gaming" ? 8 : kind === "ultra" ? 5 : 7;

    var vents = kind === "gaming"
      ? '<g fill="#0f172a" opacity=".14">'
        + '<rect x="58" y="155" width="15" height="4" rx="2"/>'
        + '<rect x="78" y="155" width="15" height="4" rx="2"/>'
        + '<rect x="98" y="155" width="15" height="4" rx="2"/>'
        + '<rect x="207" y="155" width="15" height="4" rx="2"/>'
        + '<rect x="227" y="155" width="15" height="4" rx="2"/>'
        + '<rect x="247" y="155" width="15" height="4" rx="2"/>'
        + '</g>'
      : "";

    return '<svg viewBox="24 24 272 160" class="laptop-art" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">'
      + '<defs>'
      + '<radialGradient id="glow-' + u + '" cx="50%" cy="40%" r="62%">'
      + '<stop offset="0" stop-color="' + c2 + '" stop-opacity=".42"/>'
      + '<stop offset=".6" stop-color="' + c2 + '" stop-opacity=".12"/>'
      + '<stop offset="1" stop-color="' + c2 + '" stop-opacity="0"/>'
      + '</radialGradient>'
      + '<linearGradient id="lid-' + u + '" x1="0" y1="0" x2="0" y2="1">'
      + '<stop offset="0" stop-color="#3a465c"/><stop offset="1" stop-color="#151c2a"/>'
      + '</linearGradient>'
      + '<linearGradient id="deck-' + u + '" x1="0" y1="0" x2="1" y2="0">'
      + '<stop offset="0" stop-color="#aeb9ca"/><stop offset=".5" stop-color="#e9eff7"/><stop offset="1" stop-color="#a8b4c6"/>'
      + '</linearGradient>'
      + '<linearGradient id="scr-' + u + '" x1="0" y1="0" x2="1" y2="1">'
      + '<stop offset="0" stop-color="#0a1122"/><stop offset="1" stop-color="#17253f"/>'
      + '</linearGradient>'
      + '</defs>'

      + '<rect width="320" height="200" fill="url(#glow-' + u + ')"/>'
      + '<ellipse cx="160" cy="' + (baseY + baseH + 2) + '" rx="93" ry="5" fill="#0f172a" opacity=".13"/>'

      + '<rect x="62" y="34" width="196" height="112" rx="10" fill="url(#lid-' + u + ')"/>'
      + '<rect x="68" y="40" width="184" height="100" rx="5" fill="#05090f"/>'
      + '<rect x="72" y="44" width="176" height="92" rx="3" fill="url(#scr-' + u + ')"/>'
      + '<circle cx="160" cy="37.2" r="1.3" fill="#0b1220" opacity=".55"/>'

      + content(kind, c2)
      + '<path d="M72 44h176v92z" fill="#ffffff" opacity=".022"/>'
      + '<rect x="116" y="145.5" width="88" height="2.5" rx="1.2" fill="#0d1421" opacity=".75"/>'

      + '<rect x="46" y="' + baseY + '" width="228" height="' + baseH + '" rx="' + baseR + '" fill="url(#deck-' + u + ')"/>'
      + '<rect x="52" y="' + (baseY + 1) + '" width="216" height="1.6" rx=".8" fill="#ffffff" opacity=".5"/>'
      + '<rect x="148" y="' + (baseY + 3) + '" width="24" height="2.6" rx="1.3" fill="#7c8798" opacity=".55"/>'
      + vents

      + '</svg>';
  }

  function fromLaptop(l, uid) {
    var p = palette(l.grad);
    return art(kindOf(l), p[0], p[1], uid);
  }

  global.laptopArt = { fromLaptop: fromLaptop, svg: art, kindOf: kindOf };

  function initSlots() {
    var slots = document.querySelectorAll("[data-art]");
    for (var i = 0; i < slots.length; i++) {
      var el = slots[i];
      var c1 = el.getAttribute("data-c1") || FALLBACK[0];
      var c2 = el.getAttribute("data-c2") || c1;
      el.innerHTML = art(el.getAttribute("data-art"), c1, c2, "slot" + i);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initSlots);
  } else {
    initSlots();
  }
})(window);
