function renderAdminNav(active) {
  const host = document.querySelector('#admin-nav');
  if (!host) return;
  const items = [
    ['dashboard.html', 'dashboard', 'home', 'Overview'],
    ['items.html', 'items', 'list', 'Reports'],
    ['users.html', 'users', 'user', 'Users'],
    ['reports.html', 'reports', 'flag', 'Flags'],
    ['statistics.html', 'statistics', 'chart', 'Statistics'],
  ];
  host.innerHTML = items.map(([href, key, iconName, label]) => `<a class="btn ${key === active ? 'btn-primary' : 'btn-outline'} btn-sm" href="${href}">${icon(iconName, 16)}<span>${label}</span></a>`).join('');
}
