renderAdminNav('reports');

async function loadReports() {
  const container = document.querySelector('#list');
  const { data } = await apiRequest('/admin/reports');

  if (data.reports.length === 0) {
    renderEmptyState(container, 'No flagged reports.');
    return;
  }

  container.innerHTML = data.reports.map((report) => `
    <article class="card">
      <div class="row-between">
        <div>
          <span class="badge badge-warning">${escapeHtml(report.reason)}</span>
          <h3 class="mt-4">${escapeHtml(report.item_name || `Item #${report.item_id}`)}</h3>
        </div>
        ${statusBadge(report.status)}
      </div>
      ${report.description ? `<p>${escapeHtml(report.description)}</p>` : ''}
      <p class="item-meta">Flagged by user #${report.reporter_id} · ${formatDateTime(report.created_at)}</p>
      <div class="row mt-4">
        <a class="btn btn-outline btn-sm" href="../item.html?id=${report.item_id}">${icon('eye', 16)}View item</a>
        <select class="select" style="width: auto;" data-id="${report.id}">
          ${['PENDING', 'REVIEWED', 'DISMISSED', 'ACTIONED'].map((status) => `<option value="${status}" ${status === report.status ? 'selected' : ''}>${status}</option>`).join('')}
        </select>
      </div>
    </article>
  `).join('');

  container.querySelectorAll('select[data-id]').forEach((select) => {
    select.addEventListener('change', async () => {
      try {
        await apiRequest(`/admin/reports/${select.dataset.id}`, { method: 'PUT', body: JSON.stringify({ status: select.value }) });
      } catch (error) {
        renderErrorState(container, error.message);
      }
    });
  });
}

loadReports().catch((error) => renderErrorState(document.querySelector('#list'), error.message));
