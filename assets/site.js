// Hero map: Africa drawn in logo cubes. It grows in once, then sits still until the cursor is over it.
(() => {
  const canvas = document.getElementById("field");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const AFRICA = [[-5.9,35.8],[-2,35.1],[3,36.9],[10,37.3],[10.2,34],[15,32.4],[19.9,30.5],[20,32.5],[25,31.7],[32,31.2],[34.5,28],[35.5,24],[37.2,21],[39.5,15.5],[43.2,11.5],[51.2,11.8],[49,6.5],[45.3,2],[41.5,-2],[39.5,-6],[40.5,-11],[40.6,-15.5],[35,-20],[35.5,-24],[32.7,-26],[30,-31.5],[25.5,-34],[20,-34.8],[18.3,-33.5],[15,-27],[14.4,-22.5],[11.8,-17],[13.7,-11],[12,-5],[9,-1],[9.5,3.5],[6,4.3],[3.4,6.3],[-2,5],[-4.5,5.2],[-7.5,4.4],[-11.5,7],[-13.5,9.5],[-16.8,12.5],[-17.5,14.7],[-16.3,19],[-17,21],[-14.5,26],[-10,29.5],[-9.7,31.5],[-7.5,33.6]];
  const MADAGASCAR = [[49.3,-12],[50.4,-15.5],[47.5,-24.8],[45,-25.5],[43.4,-22],[44.4,-16.5]];
  const inside = (poly, x, y) => {
    let c = false;
    for (let a = 0, b = poly.length - 1; a < poly.length; b = a++) {
      const [xa, ya] = poly[a], [xb, yb] = poly[b];
      if ((ya > y) !== (yb > y) && x < (xb - xa) * (y - ya) / (yb - ya) + xa) c = !c;
    }
    return c;
  };
  // Member cities. Each label sits out in open water at the end of a thin line, so the map itself stays clean.
  // p = the city, via = where the line runs, text = where the name sits (all lon, lat).
  const CITIES = [
    // West Africa steps down into the open Atlantic, one name per row, so nothing sits on the blocks
    { name: "Accra", country: "ghana", stat: "$270M", facts: ["Ghana launched its National AI Strategy (2025–2035) in Accra in April 2026, backed by about $270M.", "$250M of it goes to a national AI computing centre.", "Google opened its first African AI research centre in Accra in 2019."], p: [-0.19, 5.6], via: [[-0.19, 1.5]], text: [-0.9, 1.5], align: "right" },
    { name: "Lagos", country: "nigeria", stat: "88%", facts: ["88% of Nigerian adults have used an AI chatbot, up 18 points in a year (Google/Ipsos, 2025).", "10.1% of working-age Nigerians use generative AI regularly (Microsoft, early 2026).", "Nigeria has 120+ AI startups, most of them in Lagos."], p: [3.4, 6.5], via: [[3.4, -2.5]], text: [2.7, -2.5], align: "right" },
    { name: "Oyo", country: "nigeria", stat: "3M", facts: ["Nigeria's 3MTT programme aims to train 3 million tech workers across all states, Oyo included.", "Nigeria released a draft National AI Strategy in August 2024."], p: [3.93, 7.85], via: [[5.2, 7.85], [5.2, -6.5]], text: [4.5, -6.5], align: "right" },
    { name: "Yaoundé", country: "cameroon", stat: "12,000", facts: ["Cameroon's AI strategy, presented in Yaoundé in July 2025, aims to create 12,000 direct jobs by 2040.", "It plans to train 4,000 people in AI every year."], p: [11.52, 3.87], via: [[7.2, 3.87], [7.2, -10.5]], text: [6.5, -10.5], align: "right" },
    { name: "Dakar", country: "senegal", stat: "$2B", facts: ["Senegal's New Deal Technologique (February 2025) makes AI a core pillar, with about $2B planned to 2034.", "Dakar hosted the 2024 Deep Learning Indaba, Africa's biggest gathering of AI researchers.", "Senegal adopted a national AI strategy in 2023."], p: [-17.4, 14.7], via: [[-19, 14.7], [-19, 10.8]], text: [-19, 8.4], align: "center" },
    { name: "Cairo", country: "egypt", stat: "14.8%", facts: ["14.8% of working-age Egyptians use generative AI (Microsoft, early 2026).", "Egypt's 2025–2030 AI strategy targets 30,000 AI professionals and 250+ AI startups."], p: [31.2, 30], via: [[45, 30]], text: [45.7, 30], align: "left" },
    { name: "Addis Ababa", country: "ethiopia", stat: "+42%", facts: ["Ethiopia's AI institute got 1.13 billion birr in the July 2025 budget, up 42% on the year before.", "Ethiopia approved its first national AI policy in July 2024.", "An AI innovation hub with UNDP and Addis Ababa University opened in February 2026."], p: [38.7, 9], via: [[38.7, 15], [45, 15]], text: [45.7, 15], align: "left" },
    { name: "Nairobi", country: "kenya", stat: "96%", facts: ["96% of Kenyan firms surveyed have started using AI; 35% use it widely (Zoho/Arion, 2025).", "8.7% of working-age Kenyans use generative AI regularly (Microsoft, early 2026).", "Kenya's National AI Strategy, launched in Nairobi in March 2025, needs KSh 152B by 2030."], p: [36.8, -1.3], via: [[45, -1.3]], text: [45.7, -1.3], align: "left" },
    { name: "Johannesburg", country: "southafrica", stat: "23.1%", facts: ["23.1% of working-age South Africans use AI, the highest in Africa (Microsoft, early 2026).", "70% of South African adults have used an AI chatbot (Google/Ipsos, 2025).", "Microsoft opened Africa's first hyperscale cloud data centres here and in Cape Town in 2019."], p: [28, -26.2], via: [[36, -28]], text: [36.7, -28], align: "left" },
  ];
  // Countries with a marked city: rough borders (lon, lat) that only need to be right at the size of one cube.
  // Share of NCS members in each city. Leave a city out until there's a real number; the card only shows it when set.
  const MEMBERS = {};
  const COUNTRIES = {
    nigeria: { name: "Nigeria", def: "Africa's most populous country, on the Gulf of Guinea. Its capital is Abuja and its largest city is Lagos.",
      shape: [[2.7,6.4],[4.5,6.2],[5.5,4.4],[7,4.3],[8.5,4.6],[9.6,6.5],[11.2,6.6],[11.8,7.4],[12.8,8.7],[13.6,10.9],[14.1,13],[13.6,13.7],[12,13.1],[10,13.3],[7.8,13.3],[5.3,13.8],[4,13.4],[3.6,11.7],[2.7,8.5]] },
    ghana: { name: "Ghana", def: "A West African country on the Gulf of Guinea, among the first in sub-Saharan Africa to win independence, in 1957. Its capital is Accra.",
      shape: [[-3.1,5.1],[-2,4.75],[1.2,6.05],[.6,8],[.6,11.1],[-2.8,11],[-2.7,9],[-3.2,6.5]] },
    cameroon: { name: "Cameroon", def: "A Central African country where French and English are both official languages. Its capital is Yaoundé and its largest city is Douala.",
      shape: [[8.5,4.6],[9.7,3.9],[9.8,2.3],[16.1,2],[14.6,4.6],[15.5,7.5],[15.1,10],[14.6,12],[14.1,13],[13.6,10.9],[12.8,8.7],[11.8,7.4],[11.2,6.6],[9.6,6.5]] },
    senegal: { name: "Senegal", def: "West Africa's westernmost country, on the Atlantic. French is the official language and Wolof is widely spoken. Its capital is Dakar.",
      shape: [[-17.5,14.7],[-16.5,16],[-14.5,16.6],[-12.2,14.8],[-11.4,12.4],[-13.7,12.6],[-16.7,12.4],[-17,13.5]] },
    egypt: { name: "Egypt", def: "The north-east corner of Africa, with most of its people living along the Nile. Its capital is Cairo.",
      shape: [[25,31.6],[29,31],[32.3,31.2],[34.2,31.3],[34.9,29.5],[33.6,27.8],[34.3,26],[35.7,23.9],[36.9,22],[25,22],[25,29.3]] },
    ethiopia: { name: "Ethiopia", def: "A country in the Horn of Africa, and the continent's second most populous. Its capital is Addis Ababa.",
      shape: [[35.3,12.5],[36.5,14.3],[37.9,14.9],[40,14.5],[42.4,12.5],[41.8,11],[43,9.5],[44,9],[46.9,8],[48,8],[45,5],[43,4.9],[41.9,3.9],[40.8,4.2],[39.5,3.4],[38,3.6],[36,4.4],[35,5.4],[34.1,6.6],[33,7.9],[34,8.5],[34.1,10.5]] },
    kenya: { name: "Kenya", def: "An East African country on the Indian Ocean, where M-Pesa mobile money launched in 2007. Swahili and English are official. Its capital is Nairobi.",
      shape: [[34,4.2],[35.9,4.6],[36.9,4.4],[38.1,3.6],[39.6,3.4],[40.8,4.2],[41.9,3.9],[41,2.8],[41,-1.7],[39.2,-4.7],[37.7,-3.5],[34,-1],[33.9,.1],[34.6,1.2]] },
    southafrica: { name: "South Africa", def: "The southern tip of the continent, with a dozen official languages. Its largest city is Johannesburg.",
      shape: [[16.5,-28.6],[19,-28.9],[20,-28.4],[20,-24.8],[22.7,-25.3],[25.6,-25.7],[27.4,-23.4],[29.4,-22.2],[31.3,-22.4],[32,-25],[32.9,-26.9],[32.4,-28.5],[30.1,-31],[27.5,-33.3],[25.7,-34],[22.6,-34.1],[20,-34.8],[18.4,-34.2],[18.2,-31.7]] },
  };
  const countryAt = (lon, lat) => Object.keys(COUNTRIES).find(k => inside(COUNTRIES[k].shape, lon, lat)) || null;
  const rnd = (a, b) => { const s = Math.sin(a * 127.1 + b * 311.7) * 43758.5453; return s - Math.floor(s); };

  let W = 0, cells = [], e = 12, cw = 10, ch = 6, cities = [], raf = 0, last = 0, start = 0;
  const px = lon => ((lon + 24) / 84) * W, py = lat => ((43 - lat) / 81) * W;
  const pointer = { x: 0, y: 0, on: false };
  // The place the cursor is on: { city } or { country }, by key, so it survives a rebuild
  let active = null;
  const wrap = canvas.parentElement;
  const card = document.createElement("div");
  card.className = "map-card";
  card.setAttribute("aria-hidden", "true");
  card.innerHTML = '<span class="tag"></span><b></b><span class="stat"></span><ul></ul><p></p>';
  wrap.appendChild(card);
  const activeCountry = () => !active ? null : active.country || CITIES.find(c => c.name === active.city).country;

  function build() {
    const r = canvas.getBoundingClientRect();
    W = Math.round(r.width);
    if (!W) return;
    const dpr = Math.min(devicePixelRatio || 1, 2);
    canvas.width = W * dpr; canvas.height = W * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    e = W / 38; cw = e * .866; ch = e * .5;
    const lx = px(3.4), ly = py(6.5);   // the map grows outward from Lagos
    cells = [];
    const rows = Math.ceil(W / ch), half = Math.ceil(W / 2 / cw);
    for (let k = 0; k < rows; k++) for (let m = -half; m <= half; m++) {
      if ((m + k) & 1) continue;
      const x = W / 2 + m * cw, y = k * ch;
      const lon = -24 + (x / W) * 84, lat = 43 - (y / W) * 81;
      if (!inside(AFRICA, lon, lat) && !inside(MADAGASCAR, lon, lat)) continue;
      const q = rnd(m, k), d = Math.hypot(x - lx, y - ly);
      const c = { x, y, base: .55 + q * q * .8, cur: 0, lift: 0, delay: d * .9 + q * 160, country: countryAt(lon, lat), a: 1 };
      cells.push(c);
    }
    cities = CITIES.map(city => {
      const x = px(city.p[0]), y = py(city.p[1]);
      let cell = null, best = 1e12;
      for (const c of cells) { const d = (c.x - x) ** 2 + (c.y - y) ** 2; if (d < best) { best = d; cell = c; } }
      // The cube under a marker always belongs to that marker's country
      if (cell) cell.country = city.country;
      return { ...city, cell, a: 1 };
    });
    start = performance.now(); last = start;
    setActive(null);
    wake();
  }

  function frame(now) {
    raf = 0;
    const dt = Math.min(100, now - last) / 16.67; last = now;
    ctx.clearRect(0, 0, W, W);
    const theme = getComputedStyle(document.documentElement);
    const mapRight = theme.getPropertyValue("--map-right").trim(), mapLine = theme.getPropertyValue("--map-line").trim();
    let moving = false;
    const pr = e * 5;
    const lit = activeCountry();
    const ease = reduce ? 1 : 1 - Math.pow(.8, dt);
    for (const c of cells) {
      // Growth runs off the clock, so the map still arrives on time if frames are slow
      const g = reduce ? 1 : Math.min(1, Math.max(0, (now - start - c.delay) / 650));
      if (g < 1) moving = true;
      let want = 0;
      if (pointer.on && !reduce) { const d = Math.hypot(c.x - pointer.x, c.y - pointer.y); if (d < pr) want = (1 - d / pr) * 1.1; }
      c.lift += (want - c.lift) * (1 - Math.pow(.86, dt));
      if (Math.abs(want - c.lift) > .004) moving = true;
      c.cur = c.base * (1 - (1 - g) ** 3) + c.lift;
      // Everything except the chosen country steps back, which draws its shape
      const wantA = lit && c.country !== lit ? .22 : 1;
      c.a += (wantA - c.a) * ease;
      if (Math.abs(wantA - c.a) > .004) moving = true;
      if (c.cur < .02) continue;
      ctx.globalAlpha = c.a;
      const s = Math.min(1, c.cur / .4), w = cw * s + .3, v = ch * s + .2, top = c.y - c.cur * e, x = c.x, y = c.y;
      ctx.fillStyle = "#A86C48"; ctx.beginPath(); ctx.moveTo(x - w, top); ctx.lineTo(x, top + v); ctx.lineTo(x, y + v); ctx.lineTo(x - w, y); ctx.fill();
      ctx.fillStyle = mapRight; ctx.beginPath(); ctx.moveTo(x, top + v); ctx.lineTo(x + w, top); ctx.lineTo(x + w, y); ctx.lineTo(x, y + v); ctx.fill();
      ctx.fillStyle = "#5ECDCB"; ctx.beginPath(); ctx.moveTo(x, top - v); ctx.lineTo(x + w, top); ctx.lineTo(x, top + v); ctx.lineTo(x - w, top); ctx.fill();
    }
    ctx.globalAlpha = 1;
    // City markers fade in once the map has grown
    const show = reduce ? 1 : Math.min(1, Math.max(0, (now - start - 900) / 500));
    if (show < 1) moving = true;
    if (show > 0 && cities.length) {
      const fs = Math.max(10.5, W * .0205), r = Math.max(2.6, W * .0062);
      ctx.save();
      for (const c of cities) {
        const on = !active || (active.city ? active.city === c.name : active.country === c.country);
        c.a += ((on ? 1 : .3) - c.a) * ease;
        if (Math.abs((on ? 1 : .3) - c.a) > .004) moving = true;
      }
      ctx.font = `700 ${fs}px "Open Sans", Arial, sans-serif`;
      if ("fontStretch" in ctx) ctx.fontStretch = "condensed";
      if ("letterSpacing" in ctx) ctx.letterSpacing = ".03em";
      ctx.textBaseline = "middle";
      ctx.strokeStyle = mapLine; ctx.lineWidth = 1;
      for (const c of cities) {
        const y0 = c.cell ? c.cell.y - c.cell.cur * e : py(c.p[1]), x0 = px(c.p[0]);
        ctx.globalAlpha = show * c.a;
        ctx.beginPath(); ctx.moveTo(x0, y0);
        c.via.forEach(([lon, lat], k) => {
          // The first leg stays level with the raised marker when it runs sideways
          ctx.lineTo(px(lon), lat === c.p[1] ? y0 : py(lat));
        });
        ctx.stroke();
      }
      for (const c of cities) {
        const y0 = c.cell ? c.cell.y - c.cell.cur * e : py(c.p[1]), x0 = px(c.p[0]);
        ctx.globalAlpha = show * c.a;
        ctx.fillStyle = "#FFFFFF"; ctx.beginPath(); ctx.arc(x0, y0, r + 1.6, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = "#1E1F26"; ctx.beginPath(); ctx.arc(x0, y0, r, 0, Math.PI * 2); ctx.fill();
        ctx.textAlign = c.align;
        const last = c.via[c.via.length - 1];
        const ty = c.text[1] === c.p[1] && last[1] === c.p[1] ? y0 : py(c.text[1]);
        const label = c.name.toUpperCase(), tx = px(c.text[0]), tw = ctx.measureText(label).width;
        ctx.fillStyle = mapLine; ctx.fillText(label, tx, ty);
        // Remember where this was drawn, so the cursor can find it
        c.box = { x0, y0, left: c.align === "right" ? tx - tw : c.align === "center" ? tx - tw / 2 : tx, width: tw, ty, fs };
      }
      ctx.restore();
    }
    if (moving) wake();
  }
  function wake() { if (!raf) raf = requestAnimationFrame(frame); }

  // What is under the cursor? A city's marker or name first, then the country its cubes belong to.
  function hit(x, y) {
    let city = null, best = Math.max(11, W * .022);
    for (const c of cities) {
      if (!c.box) continue;
      const b = c.box, rest = c.cell ? c.cell.y - c.cell.base * e : b.y0;
      const d = Math.min(Math.hypot(x - b.x0, y - b.y0), Math.hypot(x - b.x0, y - rest));
      if (d < best) { best = d; city = c; }
    }
    if (city) return { city: city.name };
    for (const c of cities) {
      if (!c.box) continue;
      const b = c.box, pad = 5;
      if (x >= b.left - pad && x <= b.left + b.width + pad && Math.abs(y - b.ty) <= b.fs * .5 + pad) return { city: c.name };
    }
    // Measure against each cube's resting top, so the lift under the cursor can't make the answer flicker
    let cell = null, near = e * 1.1;
    for (const c of cells) {
      const d = Math.hypot(x - c.x, y - (c.y - (c.base + .3) * e));
      if (d < near) { near = d; cell = c; }
    }
    return cell && cell.country ? { country: cell.country } : null;
  }
  function setActive(next) {
    const same = (!next && !active) || (next && active && next.city === active.city && next.country === active.country);
    if (same) return;
    active = next;
    card.classList.toggle("on", !!next);
    if (next) {
      const city = next.city && CITIES.find(c => c.name === next.city);
      const home = COUNTRIES[city ? city.country : next.country];
      const names = CITIES.filter(c => c.country === next.country).map(c => c.name).join(", ");
      card.querySelector(".tag").textContent = city ? `City in ${home.name}` : `Marked here: ${names}`;
      card.querySelector("b").textContent = city ? city.name : home.name;
      const p = card.querySelector("p");
      p.textContent = city ? "" : home.def;
      p.hidden = !!city;
      const share = city ? MEMBERS[city.name] : CITIES.filter(c => c.country === next.country).reduce((t, c) => MEMBERS[c.name] != null ? (t || 0) + MEMBERS[c.name] : t, null);
      const facts = (city && city.facts ? city.facts.slice() : []);
      if (share != null) facts.unshift(`${share}% of NCS members are here.`);
      const ul = card.querySelector("ul");
      ul.replaceChildren(...facts.map(t => Object.assign(document.createElement("li"), { textContent: t })));
      ul.hidden = !facts.length;
      const st = card.querySelector(".stat");
      st.textContent = city && city.stat ? city.stat : "";
      st.hidden = !(city && city.stat);
      card.querySelector(".tag").textContent = city ? `${home.name} · AI and automation` : `Marked here: ${names}`;
    }
    wake();
  }
  // The card sits beside the point, on whichever side has room, and never leaves the map
  function placeCard(x, y) {
    const w = card.offsetWidth, h = card.offsetHeight, gap = 18;
    let left = x + gap, top = y - h - gap;
    if (left + w > W) left = x - w - gap;
    if (left < 0) left = Math.max(0, Math.min(W - w, x - w / 2));
    if (top < 0) top = y + gap;
    if (top + h > W) top = Math.max(0, W - h);
    card.style.transform = `translate(${Math.round(left)}px, ${Math.round(top)}px)`;
  }
  const at = ev => { const r = canvas.getBoundingClientRect(); return [ev.clientX - r.left, ev.clientY - r.top]; };
  canvas.addEventListener("pointermove", ev => {
    if (ev.pointerType === "touch") return;
    const [x, y] = at(ev);
    pointer.x = x; pointer.y = y; pointer.on = true;
    setActive(hit(x, y));
    if (active) placeCard(x, y);
    wake();
  });
  canvas.addEventListener("pointerleave", ev => { if (ev.pointerType === "touch") return; pointer.on = false; setActive(null); wake(); });
  // On a phone there is no cursor, so a tap does the same job, and a tap anywhere else closes it
  canvas.addEventListener("click", ev => {
    const [x, y] = at(ev);
    setActive(hit(x, y));
    if (active) placeCard(x, y);
    ev.stopPropagation();
  });
  document.addEventListener("click", () => setActive(null));
  // Keyboard and screen reader users get the same definitions, one tab stop per city
  const keys = document.createElement("div");
  keys.className = "map-keys";
  CITIES.forEach(city => {
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = `${city.name}: ${city.def}`;
    b.addEventListener("focus", () => {
      setActive({ city: city.name });
      const c = cities.find(k => k.name === city.name);
      if (c && c.box) placeCard(c.box.x0, c.box.y0);
    });
    b.addEventListener("blur", () => setActive(null));
    keys.appendChild(b);
  });
  wrap.appendChild(keys);
  // Redraw straight away when the theme changes
  new MutationObserver(wake).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", wake);
  let lastW = 0;
  new ResizeObserver(() => { const w = canvas.getBoundingClientRect().width; if (Math.abs(w - lastW) > 1) { lastW = w; build(); } }).observe(canvas);
  if (document.fonts) document.fonts.ready.then(wake);
})();

// Phone menu
(() => {
  const btn = document.querySelector(".menu-btn"), menu = document.getElementById("menu");
  if (!btn) return;
  btn.addEventListener("click", () => { const open = menu.hidden; menu.hidden = !open; btn.setAttribute("aria-expanded", open); btn.textContent = open ? "Close" : "Menu"; });
})();

// Countdown to the next cohort
(() => {
  const timers = [...document.querySelectorAll(".countdown")];
  if (!timers.length) return;
  const pad = n => String(n).padStart(2, "0");
  function tick() {
    for (const t of timers) {
      const left = new Date(t.dataset.target).getTime() - Date.now();
      if (left <= 0) {
        t.querySelector(".clock").hidden = true;
        t.querySelector(".tag").textContent = "The cohort has started. Join the waitlist for the next one.";
        continue;
      }
      const s = Math.floor(left / 1000);
      const parts = { days: Math.floor(s / 86400), hours: Math.floor(s / 3600) % 24, minutes: Math.floor(s / 60) % 60, seconds: s % 60 };
      for (const k in parts) t.querySelector(`[data-unit="${k}"]`).textContent = k === "days" ? parts[k] : pad(parts[k]);
    }
  }
  tick();
  setInterval(tick, 1000);
})();

// Merch cart. Kept in this visitor's browser only.
(() => {
  // Set this to a WhatsApp number in international format, digits only (for example "234..."), to send orders there.
  const ORDER_WHATSAPP = "";
  const KEY = "ncs-cart";
  const read = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; } };
  let memory = read();
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(memory)); } catch {} counts(); };
  const money = n => "₦" + n.toLocaleString("en-NG");
  const counts = () => { const n = memory.reduce((a, i) => a + i.qty, 0); document.querySelectorAll("[data-cart-count]").forEach(e => { e.textContent = n; }); };
  counts();

  // Product page
  const form = document.querySelector(".buy-form");
  if (form) {
    const art = document.querySelector(".big-tile .mock");
    // Products with real photos: each colour has its own pictures
    const gallery = document.querySelector(".gallery");
    if (gallery) {
      const photos = JSON.parse(gallery.dataset.photos), main = gallery.querySelector("img"), thumbs = gallery.querySelector(".thumbs");
      const showColour = colour => {
        const list = photos[colour] || [];
        main.src = list[0];
        main.alt = `${gallery.dataset.name} in ${colour.toLowerCase()}`;
        thumbs.replaceChildren();
        if (list.length < 2) return;
        list.forEach((src, k) => {
          const b = document.createElement("button");
          b.type = "button";
          b.setAttribute("aria-label", `Photo ${k + 1} of ${list.length}`);
          b.setAttribute("aria-pressed", k === 0);
          const im = document.createElement("img"); im.src = src; im.alt = ""; b.appendChild(im);
          b.addEventListener("click", () => { main.src = src; thumbs.querySelectorAll("button").forEach(o => o.setAttribute("aria-pressed", o === b)); });
          thumbs.appendChild(b);
        });
      };
      showColour(form.querySelector('[name="colour"]:checked, input[type="hidden"][name="colour"]').value);
      form.querySelectorAll('input[type="radio"][name="colour"]').forEach(r => r.addEventListener("change", () => showColour(r.value)));
    }
    if (!gallery) form.querySelectorAll('input[type="radio"][name="colour"]').forEach(r => r.addEventListener("change", () => {
      art.style.setProperty("--garment", r.dataset.garment);
      art.style.setProperty("--print", r.dataset.print);
      art.style.setProperty("--cube-right", r.dataset.cube);
      art.setAttribute("aria-label", `Drawing of the ${form.dataset.name} in ${r.value.toLowerCase()}`);
    }));
    form.addEventListener("submit", ev => {
      ev.preventDefault();
      const d = new FormData(form), qty = Math.min(50, Math.max(1, parseInt(d.get("qty"), 10) || 1));
      const item = { id: form.dataset.id, name: form.dataset.name, price: +form.dataset.price, usd: +form.dataset.usd, kes: +form.dataset.kes, href: form.dataset.href, colour: d.get("colour"), size: d.get("size"), qty };
      const same = memory.find(i => i.id === item.id && i.colour === item.colour && i.size === item.size);
      if (same) same.qty += qty; else memory.push(item);
      save();
      const msg = form.querySelector(".added");
      msg.textContent = `Added to your cart: ${qty} × ${item.name}.`;
      msg.hidden = false;
    });
  }

  // Cart page
  const lines = document.getElementById("cartLines");
  if (!lines) return;
  const orderForm = document.getElementById("orderForm"), result = document.getElementById("orderResult");
  const total = () => memory.reduce((a, i) => a + i.price * i.qty, 0);
  const sum = key => memory.reduce((a, i) => a + (i[key] || 0) * i.qty, 0);
  // The currency switch at the bottom of this file picks which of these to show
  const setPrices = (el, ngn, usd, kes) => {
    el.dataset.prices = "";
    el.dataset.naira = money(ngn);
    if (usd) { el.dataset.dollars = "$" + usd.toLocaleString("en-US"); el.dataset.shillings = "KSh " + kes.toLocaleString("en-US"); }
    el.textContent = money(ngn);
  };
  const others = (usd, kes) => `$${usd.toLocaleString("en-US")} / KSh ${kes.toLocaleString("en-US")}`;
  function render() {
    lines.replaceChildren();
    if (!memory.length) {
      const empty = document.createElement("div");
      empty.className = "cart-empty";
      empty.innerHTML = '<p>Your cart is empty.</p><a class="slab" href="merch.html">Back to the shop</a>';
      lines.append(empty);
    }
    memory.forEach((it, idx) => {
      const row = document.createElement("div");
      row.className = "cart-line";
      const info = document.createElement("div");
      const a = document.createElement("a"); a.href = it.href; a.textContent = it.name;
      const meta = document.createElement("small"); meta.textContent = [it.colour, it.size].filter(v => v && v !== "One size" && v !== "Mixed").join(" / ");
      info.append(a, meta);
      const qty = document.createElement("div"); qty.className = "stepper";
      const btn = (label, aria, fn) => { const b = document.createElement("button"); b.type = "button"; b.textContent = label; b.setAttribute("aria-label", aria); b.addEventListener("click", fn); return b; };
      const n = document.createElement("span"); n.textContent = it.qty;
      qty.append(
        btn("−", `Remove one ${it.name}`, () => { it.qty--; if (it.qty < 1) memory.splice(idx, 1); save(); render(); }),
        n,
        btn("+", `Add one ${it.name}`, () => { it.qty = Math.min(50, it.qty + 1); save(); render(); })
      );
      const price = document.createElement("b"); setPrices(price, it.price * it.qty, (it.usd || 0) * it.qty, (it.kes || 0) * it.qty);
      const rm = btn("Remove", `Remove ${it.name} from cart`, () => { memory.splice(idx, 1); save(); render(); }); rm.className = "rm";
      row.append(info, qty, price, rm);
      lines.append(row);
    });
    setPrices(document.getElementById("cartTotal"), total(), sum("usd"), sum("kes"));
    document.dispatchEvent(new Event("ncs-prices"));
    orderForm.querySelector('button[type="submit"]').disabled = !memory.length;
  }
  render();
  orderForm.addEventListener("submit", ev => {
    ev.preventDefault();
    if (!memory.length) return;
    const d = new FormData(orderForm);
    const text = ["Nocodesquare merch order", ...memory.map(i => `${i.qty} x ${i.name}${i.colour && i.colour !== "Mixed" ? ", " + i.colour : ""}${i.size !== "One size" ? ", " + i.size : ""}: ${money(i.price * i.qty)}`), `Total: ${money(total())} / ${others(sum("usd"), sum("kes"))}`, "", `Name: ${d.get("name")}`, `Phone: ${d.get("phone")}`, `Address: ${d.get("address")}`].join("\n");
    result.replaceChildren();
    const p = document.createElement("p");
    if (ORDER_WHATSAPP) {
      p.textContent = "One last step: send your order to us on WhatsApp.";
      const go = document.createElement("a"); go.className = "slab"; go.textContent = "Send on WhatsApp"; go.href = `https://wa.me/${ORDER_WHATSAPP}?text=${encodeURIComponent(text)}`; go.target = "_blank"; go.rel = "noopener";
      result.append(p, go);
    } else {
      p.textContent = "Online ordering isn't open yet, so this order has not been sent. Copy it below and keep it for when ordering opens.";
      const box = document.createElement("textarea"); box.id = "orderText"; box.readOnly = true; box.rows = 7; box.value = text; box.setAttribute("aria-label", "Your order");
      const copy = document.createElement("button"); copy.type = "button"; copy.className = "slab ghost"; copy.textContent = "Copy order";
      copy.addEventListener("click", () => { box.select(); (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(() => { copy.textContent = "Copied"; }, () => { copy.textContent = "Selected. Copy it manually"; }); });
      result.append(p, box, copy);
    }
    result.hidden = false;
  });
})();

// Light and dark switch. Follows the device until the visitor chooses, then remembers the choice.
(() => {
  const btn = document.querySelector(".theme-btn");
  if (!btn) return;
  const root = document.documentElement, dark = matchMedia("(prefers-color-scheme: dark)");
  const current = () => root.getAttribute("data-theme") || (dark.matches ? "dark" : "light");
  const label = () => btn.setAttribute("aria-label", current() === "dark" ? "Switch to light mode" : "Switch to dark mode");
  label();
  btn.addEventListener("click", () => {
    const next = current() === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("ncs-theme", next); } catch {}
    label();
  });
  dark.addEventListener("change", label);
})();

// Currency switch for the cohort fee and the shop: remembers the visitor's choice across the site
(() => {
  const KEY = "ncs-currency";
  let current = "Naira";
  try { current = localStorage.getItem(KEY) || current; } catch {}
  // root is one shop item when its own tabs are clicked, or the whole page when it loads
  const apply = (root, cur) => {
    root.querySelectorAll("[data-cur]").forEach(b => {
      const on = b.dataset.cur === cur;
      b.setAttribute("aria-pressed", String(on));
      const amount = on && b.dataset.fee && b.closest("[data-fee-switch]")?.querySelector("[data-fee-amount]");
      if (amount) amount.textContent = b.dataset.fee;
    });
    root.querySelectorAll("[data-prices]").forEach(el => {
      el.textContent = el.dataset[cur.toLowerCase()] || el.dataset.naira || el.textContent;
    });
  };
  document.addEventListener("click", ev => {
    const b = ev.target.closest("[data-cur]");
    if (!b) return;
    current = b.dataset.cur;
    try { localStorage.setItem(KEY, current); } catch {}
    apply(b.closest("[data-cur-scope]") || document, current);
  });
  document.addEventListener("ncs-prices", () => apply(document, current));
  apply(document, current);
})();

// Favicon: follows the visitor's browser or system mode (not the site's own switch), and changes live if they switch
(() => {
  const dark = matchMedia("(prefers-color-scheme: dark)");
  const set = () => {
    document.querySelectorAll('link[rel~="icon"]').forEach(l => l.remove());
    const link = document.createElement("link");
    link.rel = "icon"; link.type = "image/png"; link.sizes = "64x64";
    link.href = dark.matches ? "favicon-dark.png" : "favicon-light.png";
    document.head.append(link);
  };
  set();
  dark.addEventListener("change", set);
})();

// Human or Machine: Machine swaps the page for its Markdown copy, which is what an AI agent reads
(() => {
  const switches = document.querySelectorAll(".mode-switch");
  const md = document.body.dataset.md;
  if (!switches.length || !md) return;
  const KEY = "ncs-mode";
  let view = null, loaded = false;
  function build() {
    view = document.createElement("section");
    view.className = "machine-view";
    view.hidden = true;
    view.innerHTML = `<div class="machine-inner">
      <div class="machine-bar">
        <button type="button" class="machine-copy">Copy to clipboard</button>
        <a class="machine-raw" href="${md}">Open ${md}</a>
        <a class="machine-raw" href="llms.txt">Whole site: llms.txt</a>
      </div>
      <pre class="machine-text" tabindex="0" aria-label="This page as Markdown">Loading…</pre>
    </div>`;
    document.querySelector("header.nav").after(view);
    const pre = view.querySelector(".machine-text"), copy = view.querySelector(".machine-copy");
    copy.addEventListener("click", () => {
      const done = () => { copy.textContent = "Copied"; setTimeout(() => { copy.textContent = "Copy to clipboard"; }, 1600); };
      if (navigator.clipboard) navigator.clipboard.writeText(pre.textContent).then(done, () => select(pre));
      else select(pre);
    });
  }
  function select(el) {
    const r = document.createRange(); r.selectNodeContents(el);
    const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r);
  }
  function load() {
    if (loaded) return;
    loaded = true;
    const pre = view.querySelector(".machine-text");
    fetch(md).then(r => { if (!r.ok) throw 0; return r.text(); })
      .then(t => { pre.textContent = t; })
      .catch(() => { loaded = false; pre.textContent = "This page's Markdown couldn't load here. Open it directly: " + md; });
  }
  function set(mode, save) {
    const machine = mode === "machine";
    if (machine && !view) build();
    document.documentElement.classList.toggle("is-machine", machine);
    if (view) view.hidden = !machine;
    if (machine) load();
    document.querySelectorAll(".mode-switch [data-mode]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.mode === mode)));
    if (save) { try { localStorage.setItem(KEY, mode); } catch {} }
  }
  document.addEventListener("click", ev => {
    const b = ev.target.closest(".mode-switch [data-mode]");
    if (!b) return;
    set(b.dataset.mode, true);
    window.scrollTo(0, 0);
  });
  let saved = "human";
  try { saved = localStorage.getItem(KEY) || saved; } catch {}
  if (saved === "machine") set("machine", false);
})();

// Newsletter sign-up: posts the email to the webhook set in build_site.py (NEWSLETTER_WEBHOOK)
(() => {
  document.querySelectorAll(".nl-form").forEach(form => {
    const input = form.querySelector("input[type=email]");
    const btn = form.querySelector("button");
    const msg = form.querySelector(".nl-msg");
    const say = (text, kind) => { msg.textContent = text; msg.className = "nl-msg" + (kind ? " " + kind : ""); };
    form.addEventListener("submit", async ev => {
      ev.preventDefault();
      const email = input.value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { say("Please enter a valid email address.", "err"); input.focus(); return; }
      const endpoint = form.dataset.endpoint;
      if (!endpoint) { say("Newsletter sign-ups open soon. Follow us on LinkedIn for news until then.", "err"); return; }
      btn.disabled = true; say("Subscribing…");
      try {
        const res = await fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, page: location.pathname, source: "footer" }) });
        if (!res.ok) throw new Error(res.status);
        say("You're in. Watch your inbox for the next issue.", "ok");
        form.reset();
      } catch {
        say("That didn't go through. Please try again in a moment.", "err");
      } finally { btn.disabled = false; }
    });
  });
})();

