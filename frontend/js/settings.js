async function loadSettings() {
  const { data } = await apiRequest('/auth/profile');
  const user = data.user;
  document.querySelector('#name').value = user.name;
  document.querySelector('#department').value = user.department;
  document.querySelector('#phone').value = user.phone || '';
}

document.querySelector('#settings-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const status = document.querySelector('#settings-message');
  try {
    await apiRequest('/auth/profile', {
      method: 'PUT',
      body: JSON.stringify({
        name: document.querySelector('#name').value,
        department: document.querySelector('#department').value,
        phone: document.querySelector('#phone').value,
      }),
    });
    status.className = 'alert alert-success';
    status.textContent = 'Profile updated.';
  } catch (error) {
    status.className = 'alert alert-danger';
    status.textContent = error.message;
  }
});

document.querySelector('#logout').addEventListener('click', async () => {
  await apiRequest('/auth/logout', { method: 'POST' });
  location.href = 'index.html';
});

loadSettings().catch((error) => {
  const status = document.querySelector('#settings-message');
  status.className = 'alert alert-danger';
  status.textContent = error.message;
});
