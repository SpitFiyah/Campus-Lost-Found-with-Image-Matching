async function loadDashboard() {
  const session = await layoutReady;
  if (!session || !session.authenticated) {
    window.location.href = 'login.html';
    return;
  }

  document.querySelector('#user-name').textContent = session.user.name;

  const [mine, notifications] = await Promise.all([
    apiRequest(`/items?user_id=${session.user.id}`),
    apiRequest('/notifications'),
  ]);

  const items = mine.data.items;
  document.querySelector('#item-count').textContent = items.length;
  document.querySelector('#lost-count').textContent = items.filter((item) => item.type === 'LOST').length;
  document.querySelector('#found-count').textContent = items.filter((item) => item.type === 'FOUND').length;
  document.querySelector('#notification-count').textContent = notifications.data.unread_count;

  const recent = document.querySelector('#recent-reports');
  if (items.length === 0) {
    renderEmptyState(recent, "You haven't reported any items yet.");
    return;
  }
  recent.innerHTML = items.slice(0, 5).map((item) => `
    <div class="row-between card" style="margin-bottom: var(--space-3);">
      <div>
        ${typeBadge(item.type)}
        <strong style="margin-left: var(--space-2);">${escapeHtml(item.name)}</strong>
        <p class="item-meta mt-0">${escapeHtml(item.location)} · ${formatDate(item.date_lost_found)}</p>
      </div>
      <a class="btn btn-outline btn-sm" href="item.html?id=${item.id}">${icon('eye', 16)}View</a>
    </div>
  `).join('');
}

loadDashboard().catch((error) => {
  const banner = document.querySelector('#page-error');
  banner.textContent = error.message;
  banner.classList.remove('hidden');
});
