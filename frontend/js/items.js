async function loadItems() {
  const params = new URLSearchParams();
  const query = document.querySelector('#search').value.trim();
  const type = document.querySelector('#type').value;
  if (query) params.set('q', query);
  if (type) params.set('type', type);

  const container = document.querySelector('#item-list');
  renderLoadingState(container, 'Searching reports…');

  const response = await apiRequest(`/items?${params}`);
  const items = response.data.items;

  if (items.length === 0) {
    renderEmptyState(container, 'No matching reports found. Try adjusting your search.');
    return;
  }

  container.innerHTML = items.map((item) => {
    const thumb = item.images[0] ? `<img class="item-thumb" src="${imageUrl(item.images[0].image_path)}" alt="Photo of ${escapeHtml(item.name)}">` : '<div class="item-thumb"></div>';
    return `
      <article class="card item-card">
        ${thumb}
        <div>${typeBadge(item.type)} ${item.category ? `<span class="muted">${escapeHtml(item.category)}</span>` : ''}</div>
        <h3>${escapeHtml(item.name)}</h3>
        <p class="item-meta">${escapeHtml(item.location)} · ${formatDate(item.date_lost_found)}</p>
        <a href="item.html?id=${item.id}" class="btn btn-outline btn-sm">${icon('eye', 16)}View details</a>
      </article>
    `;
  }).join('');
}

document.querySelector('#search-form')?.addEventListener('submit', (event) => {
  event.preventDefault();
  loadItems().catch((error) => renderErrorState(document.querySelector('#item-list'), error.message));
});

loadItems().catch((error) => renderErrorState(document.querySelector('#item-list'), error.message));
