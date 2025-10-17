/* ===== Reset básico ===== */
*,
*::before,
*::after { box-sizing: border-box; }
html, body { height: 100%; }
body {
  margin: 0;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  line-height: 1.5;
  color: #0f172a;                 /* slate-900 */
  background: #f8fafc;            /* slate-50 */
}
img, svg, video { max-width: 100%; display: block; }
a { color: inherit; text-decoration: none; }
button, input, textarea, select { font: inherit; color: inherit; }

/* ===== Utilidades ===== */
.container { max-width: 1100px; margin: 0 auto; padding: 0 16px; }
.grid { display: grid; gap: 16px; }
.flex { display: flex; gap: 12px; }
.center { display: grid; place-items: center; }
.hidden { display: none !important; }
.muted { color: #64748b; }        /* slate-500 */
.round { border-radius: 12px; }
.shadow { box-shadow: 0 8px 20px rgba(2,6,23,.08); }

/* ===== Tipografías ===== */
h1, h2, h3 { line-height: 1.2; margin: 0 0 .6em; }
h1 { font-size: clamp(28px, 4vw, 40px); }
h2 { font-size: clamp(22px, 3vw, 30px); }
h3 { font-size: clamp(18px, 2.4vw, 24px); }
p { margin: 0 0 1em; }

/* ===== Header / Nav ===== */
.header {
  position: sticky; top: 0; z-index: 50;
  background: #ffffffcc; backdrop-filter: blur(8px);
  border-bottom: 1px solid #e2e8f0;
}
.header .wrap {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 16px;
}
.brand { font-weight: 700; display: flex; align-items: center; gap: 8px; }
.brand .logo {
  width: 24px; height: 24px; border-radius: 6px;
  background: linear-gradient(135deg,#3b82f6,#22c55e);
}
.nav { display: flex; gap: 8px; }
.nav a {
  padding: 8px 12px; border-radius: 8px; color: #0f172a;
}
.nav a:hover { background: #e2e8f0; }

/* ===== Botones ===== */
.btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 14px; border-radius: 10px; border: 1px solid #cbd5e1;
  background: #fff; color: #0f172a; font-weight: 600; cursor: pointer;
}
.btn:hover { background: #f1f5f9; }
.btn.primary {
  border-color: #3b82f6; background: #3b82f6; color: #fff;
}
.btn.success { border-color:#16a34a; background:#16a34a; color:#fff; }
.btn.ghost { background: transparent; border-color: #e2e8f0; }

/* ===== Tarjetas ===== */
.card {
  background: #fff; border: 1px solid #e2e8f0; border-radius: 14px;
  padding: 16px; box-shadow: 0 10px 18px rgba(2,6,23,.06);
}
.card h3 { margin-top: 0; }

/* ===== Formularios ===== */
.form { display: grid; gap: 12px; }
label { font-weight: 600; color: #0f172a; }
.input, .textarea, .select {
  width: 100%; padding: 10px 12px; border-radius: 10px;
  border: 1px solid #cbd5e1; background: #fff;
}
.input:focus, .textarea:focus, .select:focus {
  outline: 2px solid #93c5fd; outline-offset: 1px; border-color: #3b82f6;
}
.textarea { min-height: 120px; resize: vertical; }
.form-row {
  display: grid; grid-template-columns: repeat(12, 1fr); gap: 12px;
}
.col-6 { grid-column: span 6; }
.col-12 { grid-column: span 12; }

/* ===== Tabla ===== */
.table { width: 100%; border-collapse: collapse; background: #fff; }
.table th, .table td { padding: 12px; border-bottom: 1px solid #e2e8f0; }
.table th { text-align: left; color: #334155; background: #f8fafc; }

/* ===== Secciones ===== */
.section { padding: 32px 0; }
.hero {
  padding: 56px 0; background: linear-gradient(180deg,#f8fafc, #eef2ff);
}
.hero .actions { display:flex; gap:12px; flex-wrap:wrap; }

/* ===== Calendario simple ===== */
.calendar {
  background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; overflow: hidden;
}
.calendar .header {
  display: grid; grid-template-columns: 80px repeat(7, 1fr);
  background: #f1f5f9; border-bottom: 1px solid #e2e8f0;
}
.calendar .header div { padding: 10px; font-weight: 600; color:#334155; }
.calendar .grid {
  display: grid; grid-template-columns: 80px repeat(7, 1fr); gap: 0;
}
.calendar .hour {
  padding: 8px; color: #64748b; border-right: 1px solid #e2e8f0;
  border-bottom: 1px dashed #e2e8f0; background: #fafafa; font-size: 12px;
}
.calendar .day {
  min-height: 80px; border-bottom: 1px dashed #e2e8f0;
  border-right: 1px solid #e2e8f0; position: relative;
}
.event {
  position: absolute; left: 6px; right: 6px;
  background: #3b82f6; color: #fff; border-radius: 8px;
  padding: 6px 8px; font-size: 12px; box-shadow: 0 4px 10px rgba(59,130,246,.25);
}

/* ===== Alerts / Badges ===== */
.alert {
  padding: 12px 14px; border-radius: 10px; border: 1px solid;
  background: #fff;
}
.alert.info { border-color:#bfdbfe; color:#1d4ed8; }
.alert.warn { border-color:#fde68a; color:#b45309; background:#fffbeb; }
.badge {
  display:inline-block; padding:4px 8px; border-radius:999px;
  background:#e2e8f0; color:#0f172a; font-size:12px; font-weight:600;
}

/* ===== Footer ===== */
.footer {
  padding: 24px 0; color: #64748b; border-top: 1px solid #e2e8f0;
  background: #ffffff;
}

/* ===== Responsive ===== */
@media (max-width: 900px) {
  .form-row { grid-template-columns: 1fr; }
  .col-6, .col-12 { grid-column: 1 / -1; }
  .nav { display:none; }
}
@media (max-width: 640px) {
  .hero { padding: 32px 0; }
  .header .wrap { padding: 10px 12px; }
}
