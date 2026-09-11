renderAdminNav('statistics');

function breakdownTable(container, rows, columnLabel) {
  if (rows.length === 0) {
    renderEmptyState(container, 'No data yet.');
    return;
  }
  const key = Object.keys(rows[0])[0];
  container.innerHTML = `
    <div class="table-wrap"><table>
      <thead><tr><th>${escapeHtml(columnLabel)}</th><th>Reports</th></tr></thead>
      <tbody>${rows.map((row) => `<tr><td>${escapeHtml(row[key])}</td><td>${row.reports}</td></tr>`).join('')}</tbody>
    </table></div>
  `;
}

async function loadStatistics() {
  const { data } = await apiRequest('/admin/statistics');

  document.querySelector('#lost-found').innerHTML = [
    ['Lost reports', data.lost_reports],
    ['Found reports', data.found_reports],
    ['Pending matches', data.pending_matches],
    ['Return rate', `${data.return_rate}%`],
  ].map(([label, value]) => `<div class="stat-tile"><span class="value">${escapeHtml(String(value))}</span><span class="label">${escapeHtml(label)}</span></div>`).join('');

  breakdownTable(document.querySelector('#by-category'), data.categories, 'Category');
  breakdownTable(document.querySelector('#by-location'), data.hotspots, 'Location');
}

loadStatistics().catch((error) => renderErrorState(document.querySelector('#lost-found'), error.message));
