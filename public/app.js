let currentMode = 'vulnerable';

function selectMode(mode) {
  currentMode = mode;
  document.getElementById('btn-vuln').className = mode === 'vulnerable' ? 'active-vuln' : '';
  document.getElementById('btn-sec').className = mode === 'secure' ? 'active-sec' : '';
}

async function submitLogin() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const endpoint = currentMode === 'vulnerable' ? '/api/vulnerable-login' : '/api/secure-login';

  const sqlEl = document.getElementById('sql-display');
  const respEl = document.getElementById('response-display');

  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    
    const data = await res.json();
    sqlEl.innerText = data.executed_sql;
    respEl.innerText = data.message;
    respEl.style.color = res.ok ? '#51cf66' : '#f38ba8';
  } catch (err) {
    respEl.innerText = "Error connecting to server.";
    respEl.style.color = '#f38ba8';
  }
}