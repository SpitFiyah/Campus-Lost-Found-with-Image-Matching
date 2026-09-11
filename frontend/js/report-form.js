const reportType = (new URLSearchParams(location.search).get('type') || 'LOST').toUpperCase() === 'FOUND' ? 'FOUND' : 'LOST';
document.querySelector('#report-type').value = reportType;
document.querySelector('#report-type-label').textContent = reportType.toLowerCase();

apiRequest('/items/locations').then(({ data }) => {
  const select = document.querySelector('#location');
  select.innerHTML = '<option value="">Choose a location</option>' + data.locations.map((location) => `<option>${escapeHtml(location)}</option>`).join('');
});

document.querySelector('#images').addEventListener('change', (event) => {
  const names = Array.from(event.target.files).map((file) => file.name).join(', ');
  document.querySelector('#file-names').textContent = names;
});

document.querySelector('#item-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const status = document.querySelector('#form-message');
  status.textContent = '';
  status.className = '';
  const submitButton = event.target.querySelector('button[type="submit"]');
  submitButton.disabled = true;
  try {
    await apiRequest('/items', { method: 'POST', body: new FormData(event.target) });
    location.href = 'dashboard.html';
  } catch (error) {
    status.className = 'alert alert-danger';
    status.textContent = error.message;
    submitButton.disabled = false;
  }
});
