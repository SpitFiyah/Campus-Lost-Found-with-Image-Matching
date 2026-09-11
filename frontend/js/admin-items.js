renderAdminNav('items');

async function loadItems() {
  const container = document.querySelector('#list');
  const { data } = await apiRequest('/admin/items');

  if (data.items.length === 0) {
    renderEmptyState(container, 'No reports yet.');
    return;
  }

  container.innerHTML = `
    <div class="table-wrap"><table>
      <thead><tr><th>Type</th><th>Name</th><th>Category</th><th>Location</th><th>Status</th><th>Reported by (user id)</th><th>Reported</th><th>Actions</th></tr></thead>
      <tbody>
        ${data.items.map((item) => `
          <tr>
            <td>${typeBadge(item.type)}</td>
            <td>${escapeHtml(item.name)}</td>
            <td>${escapeHtml(item.category)}</td>
            <td>${escapeHtml(item.location)}</td>
            <td>${statusBadge(item.status)}</td>
            <td>${item.user_id}</td>
            <td>${formatDate(item.created_at)}</td>
            <td><a class="btn btn-outline btn-icon btn-sm" href="../item.html?id=${item.id}" title="View item">${icon('eye', 16)}</a></td>
          </tr>
        `).join('')}
      </tbody>
    </table></div>
  `;
}

loadItems().catch((error) => renderErrorState(document.querySelector('#list'), error.message));
