
:root {
  --color-primario: #4a6cf7;
  --color-secundario: #1e293b;
  --color-fondo: #f8fafc;
  --color-texto: #1e293b;
  --color-blanco: #ffffff;
  --color-gris: #94a3b8;
  --color-exito: #22c55e;
  --color-error: #ef4444;
  --sombra: 0 4px 10px rgba(0,0,0,0.1);
  --radio: 8px;
  --trans: all 0.3s ease;
  --fuente: 'Poppins', sans-serif;
}

body {
  font-family: var(--fuente);
  background: var(--color-fondo);
  color: var(--color-texto);
  line-height: 1.6;
  margin: 0;
  padding: 0;
}


header {
  background: var(--color-primario);
  color: var(--color-blanco);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: var(--sombra);
}

header h1 {
  font-size: 1.5rem;
  letter-spacing: 1px;
}

nav a {
  color: var(--color-blanco);
  margin: 0 1rem;
  text-decoration: none;
  font-weight: 500;
  transition: var(--trans);
}

nav a:hover {
  color: #cbd5e1;
}


.btn {
  display: inline-block;
  padding: 0.7rem 1.4rem;
  border-radius: var(--radio);
  background: var(--color-primario);
  color: var(--color-blanco);
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: var(--trans);
}
.btn:hover {
  background: #3859e0;
}
.btn-secundario {
  background: var(--color-secundario);
}
.btn-secundario:hover {
  background: #0f172a;
}


.card {
  background: var(--color-blanco);
  border-radius: var(--radio);
  box-shadow: var(--sombra);
  padding: 1.5rem;
  margin: 1rem;
  transition: var(--trans);
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 18px rgba(0,0,0,0.15);
}
.card h3 {
  margin-top: 0;
}


form {
  background: var(--color-blanco);
  border-radius: var(--radio);
  padding: 2rem;
  box-shadow: var(--sombra);
  max-width: 600px;
  margin: 2rem auto;
}
label {
  display: block;
  font-weight: 500;
  margin-top: 1rem;
}
input, textarea, select {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #cbd5e1;
  border-radius: var(--radio);
  margin-top: 0.5rem;
  font-size: 1rem;
  transition: var(--trans);
}
input:focus, textarea:focus, select:focus {
  outline: none;
  border-color: var(--color-primario);
  box-shadow: 0 0 0 3px rgba(74,108,247,0.2);
}


table {
  border-collapse: collapse;
  width: 100%;
  background: var(--color-blanco);
  box-shadow: var(--sombra);
}
th, td {
  text-align: left;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}
th {
  background: var(--color-primario);
  color: var(--color-blanco);
}
tr:hover {
  background: #f1f5f9;
}


footer {
  background: var(--color-secundario);
  color: var(--color-blanco);
  text-align: center;
  padding: 1rem;
  font-size: 0.9rem;
}


.flex {
  display: flex;
  gap: 1rem;
}
.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}
.grid {
  display: grid;
  gap: 1rem;
}
.grid-2 {
  grid-template-columns: repeat(2, 1fr);
}
.grid-3 {
  grid-template-columns: repeat(3, 1fr);
}
.grid-4 {
  grid-template-columns: repeat(4, 1fr);
}


.modal {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: none;
  justify-content: center;
  align-items: center;
  z-index: 50;
}
.modal.activo {
  display: flex;
}
.modal-contenido {
  background: var(--color-blanco);
  border-radius: var(--radio);
  padding: 2rem;
  width: 90%;
  max-width: 500px;
  box-shadow: var(--sombra);
  animation: aparecer 0.3s ease;
}
@keyframes aparecer {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}


.tooltip {
  position: relative;
  display: inline-block;
}
.tooltip .tooltip-text {
  visibility: hidden;
  background: var(--color-secundario);
  color: var(--color-blanco);
  padding: 0.5rem;
  border-radius: var(--radio);
  position: absolute;
  bottom: 125%;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: var(--trans);
  width: max-content;
}
.tooltip:hover .tooltip-text {
  visibility: visible;
  opacity: 1;
}


@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.fade-in {
  animation: fadeIn 0.6s ease;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid #ccc;
  border-top: 3px solid var(--color-primario);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* ===========================
   🔹 DARK MODE
   =========================== */
@media (prefers-color-scheme: dark) {
  :root {
    --color-fondo: #0f172a;
    --color-texto: #e2e8f0;
    --color-blanco: #1e293b;
    --color-secundario: #1e293b;
  }
  header, footer {
    background: #1e293b;
  }
  .card, form, table {
    background: #1e293b;
    color: #e2e8f0;
  }
}

/* ===========================
   🔹 UTILIDADES
   =========================== */
.mt-1 { margin-top: .25rem; }
.mt-2 { margin-top: .5rem; }
.mt-3 { margin-top: 1rem; }
.mb-1 { margin-bottom: .25rem; }
.mb-2 { margin-bottom: .5rem; }
.mb-3 { margin-bottom: 1rem; }
.text-center { text-align: center; }
.text-right { text-align: right; }
.bold { font-weight: 700; }
.italic { font-style: italic; }
.oculto { display: none; }

/* ===========================
   🔹 SCROLL Y RESPONSIVE
   =========================== */
::-webkit-scrollbar {
  width: 10px;
}
::-webkit-scrollbar-thumb {
  background: var(--color-primario);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
  background: #3757cc;
}

/* Responsive */
@media (max-width: 768px) {
  .grid-2, .grid-3, .grid-4 {
    grid-template-columns: 1fr;
  }
  header {
    flex-direction: column;
    text-align: center;
  }
  nav a {
    display: block;
    margin: 0.5rem 0;
  }
}
