// Videos are preload="none" and never start on their own -- the viewer presses play.
// Nothing is fetched until then. A video that scrolls fully out of view is paused so
// it stops using bandwidth in the background.
var io = new IntersectionObserver(function(es){
  es.forEach(function(e){ if (!e.isIntersecting && !e.target.paused) e.target.pause(); });
}, {threshold: 0});
document.querySelectorAll("video").forEach(function(v){ io.observe(v); });

// The index page holds both About and Research, so the nav highlight has to follow
// the scroll position rather than the page. Subpages have no such anchors and skip this.
(function () {
  var about = document.getElementById("about");
  var research = document.getElementById("research");
  if (!about || !research) return;

  var links = {};
  document.querySelectorAll("nav.top a").forEach(function (a) {
    var m = (a.getAttribute("href") || "").match(/#(about|research)$/);
    if (m) links[m[1]] = a;
  });
  if (!links.about || !links.research) return;

  function update() {
    // whichever section has crossed just under the sticky nav is the current one
    var line = window.scrollY + 140;
    var current = research.offsetTop <= line ? "research" : "about";
    links.about.classList.toggle("on", current === "about");
    links.research.classList.toggle("on", current === "research");
  }

  update();
  window.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
})();
