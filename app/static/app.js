const question = document.querySelector('#question');
const depth = document.querySelector('#depth');
const planBtn = document.querySelector('#planBtn');
const status = document.querySelector('#status');
const output = document.querySelector('#output');

planBtn.addEventListener('click', async () => {
  const text = question.value.trim();
  if (text.length < 8) { status.textContent = 'Enter a research question of at least 8 characters.'; return; }
  planBtn.disabled = true;
  status.textContent = 'Asking the planner through Mesh API…';
  output.hidden = true;
  try {
    const response = await fetch('/api/plan', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({question: text, research_depth: depth.value})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Request failed');
    status.textContent = `Planner created ${data.tasks.length} research tasks.`;
    output.textContent = JSON.stringify(data, null, 2);
    output.hidden = false;
  } catch (error) {
    status.textContent = `Could not create plan: ${error.message}`;
  } finally { planBtn.disabled = false; }
});
