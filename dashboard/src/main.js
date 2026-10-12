import './style.css';

const app = document.querySelector('#app');

app.innerHTML = `
  <main class="shell">
    <header class="topbar">
      <div class="brand-mark">D</div>
      <div>
        <p class="eyebrow">PERSONAL AI OPERATING SYSTEM</p>
        <h1>Danny AI OS</h1>
      </div>
      <span class="status"><i></i> Local dashboard</span>
    </header>

    <section class="intro">
      <p class="eyebrow">CONTROL CENTER</p>
      <h2>Your workflows, in one place.</h2>
      <p class="muted">A minimal local dashboard. The existing Python + LangGraph workflow remains the source of truth.</p>
    </section>

    <section class="grid">
      <article class="panel">
        <p class="eyebrow">SYSTEM</p>
        <h3 id="system-state">Checking…</h3>
        <p class="muted" id="system-detail">Connecting to the Python backend.</p>
      </article>
      <article class="panel">
        <p class="eyebrow">WORKFLOW</p>
        <h3>Manager graph</h3>
        <p class="muted">Runs the current safe demo workflow. It does not execute arbitrary commands or call paid APIs.</p>
        <button id="run-workflow" type="button">Run demo workflow</button>
        <p id="run-result" class="result" role="status" aria-live="polite"></p>
      </article>
    </section>
    <footer>Development preview · Keep this service bound to localhost.</footer>
  </main>
`;

async function refreshStatus() {
  const state = document.querySelector('#system-state');
  const detail = document.querySelector('#system-detail');
  try {
    const response = await fetch('/api/status');
    if (!response.ok) throw new Error('Backend returned ' + response.status);
    const data = await response.json();
    state.textContent = data.status === 'ok' ? 'Online' : 'Unavailable';
    detail.textContent = data.workflow || 'Python backend connected.';
  } catch {
    state.textContent = 'Backend offline';
    detail.textContent = 'Start the Python dashboard API, then refresh this page.';
  }
}

document.querySelector('#run-workflow').addEventListener('click', async () => {
  const button = document.querySelector('#run-workflow');
  const result = document.querySelector('#run-result');
  button.disabled = true;
  result.textContent = 'Running…';
  try {
    const response = await fetch('/api/run', { method: 'POST' });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Workflow failed');
    result.textContent = data.message || 'Workflow completed.';
  } catch (error) {
    result.textContent = error.message || 'Could not reach the Python backend.';
  } finally {
    button.disabled = false;
  }
});

refreshStatus();
