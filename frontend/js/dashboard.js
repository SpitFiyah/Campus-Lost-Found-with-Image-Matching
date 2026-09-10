async function loadDashboard() {
  const session = await apiRequest('/auth/session');
  if (!session.data.authenticated) { window.location.href = 'login.html'; return; }
  document.querySelector('#user-name').textContent = session.data.user.name;
  const items = await apiRequest('/items');
  const mine = items.data.items.filter(item => item.user_id === session.data.user.id);
  document.querySelector('#item-count').textContent = mine.length;
  document.querySelector('#lost-count').textContent = mine.filter(item => item.type === 'LOST').length;
  document.querySelector('#found-count').textContent = mine.filter(item => item.type === 'FOUND').length;
  const notifications = await apiRequest('/notifications');
  document.querySelector('#notification-count').textContent = notifications.data.unread_count;
}
loadDashboard().catch(error => { document.querySelector('#page-error').textContent = error.message; });
