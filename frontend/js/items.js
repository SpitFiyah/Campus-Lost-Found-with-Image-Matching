async function loadItems() {
  const params = new URLSearchParams();
  const query = document.querySelector('#search').value.trim();
  const type = document.querySelector('#type').value;
  if (query) params.set('q', query);
  if (type) params.set('type', type);
  const response = await apiRequest(`/items?${params}`);
  const container = document.querySelector('#item-list');
  
  if (!response.data.items || response.data.items.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <p><i class="bi bi-search" aria-hidden="true"></i> No matching reports found yet.</p>
        <p style="font-size: 0.95rem; color: #999; margin-top: 0.5rem;">Try adjusting your search or browse all items.</p>
      </div>
    `;
    return;
  }
  
  container.innerHTML = response.data.items.map(item => {
    const badgeClass = item.type === 'LOST' ? 'badge-danger' : 'badge-success';
    const badgeColor = item.type === 'LOST' ? '#dc3545' : '#198754';
    return `
      <article class="item-card" style="border: 1px solid var(--border-light);">
        <div>
          <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.75rem;">
            <span class="badge" style="background-color: ${badgeColor}; color: white; padding: 0.5rem 1rem; font-size: 0.85rem; border-radius: 6px;">
              ${item.type}
            </span>
            ${item.category ? `<span style="color: #999; font-size: 0.9rem;">${item.category}</span>` : ''}
          </div>
          <h2 style="margin: 0.5rem 0; font-size: 1.35rem;">${item.name}</h2>
          <p style="margin: 0.5rem 0; color: #666;">
            <i class="bi bi-geo-alt" aria-hidden="true"></i> ${item.location}
          </p>
          <p style="margin: 0.5rem 0; color: #999; font-size: 0.9rem;">
            <i class="bi bi-calendar3" aria-hidden="true"></i> ${item.date_lost_found}
          </p>
        </div>
        <a href="item.html?id=${item.id}" class="btn btn-primary" style="white-space: nowrap;">
          View Details
        </a>
      </article>
    `;
  }).join('');
}

document.querySelector('#search-form')?.addEventListener('submit', event => {
  event.preventDefault();
  loadItems().catch(error => alert(error.message));
});

loadItems().catch(error => {
  document.querySelector('#item-list').innerHTML = `
    <div class="empty-state">
      <p><i class="bi bi-x-circle" aria-hidden="true"></i> ${error.message}</p>
    </div>
  `;
});
