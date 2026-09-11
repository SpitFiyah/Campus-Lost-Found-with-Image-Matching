async function loadNotifications() {
  const container = document.querySelector('#list');
  const { data } = await apiRequest('/notifications');

  if (data.notifications.length === 0) {
    renderEmptyState(container, 'No notifications yet. Check back when potential matches are found.');
    return;
  }

  container.innerHTML = data.notifications.map((notification) => `
    <article class="card" data-id="${notification.id}">
      <div class="row-between">
        <strong class="row">${icon('bell', 16)}${escapeHtml(notification.title)}</strong>
        ${notification.is_read ? '' : `<button class="btn btn-outline btn-sm" data-action="read">${icon('check', 16)}Mark read</button>`}
      </div>
      <p>${escapeHtml(notification.message)}</p>
      <p class="item-meta">${formatDateTime(notification.created_at)}</p>
    </article>
  `).join('');

  container.querySelectorAll('button[data-action="read"]').forEach((button) => {
    button.addEventListener('click', async () => {
      const card = button.closest('article');
      try {
        await apiRequest(`/notifications/${card.dataset.id}/read`, { method: 'PUT' });
        loadNotifications();
      } catch (error) {
        renderErrorState(container, error.message);
      }
    });
  });
}

loadNotifications().catch((error) => renderErrorState(document.querySelector('#list'), error.message));
