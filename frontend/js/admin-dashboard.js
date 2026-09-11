renderAdminNav('dashboard');

async function loadOverview() {
  const { data } = await apiRequest('/admin/statistics');
  document.querySelector('#stats').innerHTML = [
    ['Users', data.total_users],
    ['Reports', data.total_items],
    ['Returned', data.returned_items],
    ['Pending matches', data.pending_matches],
    ['Return rate', `${data.return_rate}%`],
  ].map(([label, value]) => `<div class="stat-tile"><span class="value">${escapeHtml(String(value))}</span><span class="label">${escapeHtml(label)}</span></div>`).join('');

  const hotspots = document.querySelector('#hotspots');
  if (data.hotspots.length === 0) {
    renderEmptyState(hotspots, 'No reports yet.');
    return;
  }
  hotspots.innerHTML = `
    <div class="table-wrap"><table>
      <thead><tr><th>Location</th><th>Reports</th></tr></thead>
      <tbody>${data.hotspots.map((row) => `<tr><td>${escapeHtml(row.location)}</td><td>${row.reports}</td></tr>`).join('')}</tbody>
    </table></div>
  `;
}

loadOverview().catch((error) => renderErrorState(document.querySelector('#stats'), error.message));
