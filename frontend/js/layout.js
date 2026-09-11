function currentPageKey() {
  const file = location.pathname.split('/').pop() || 'index.html';
  return file.replace('.html', '') || 'index';
}

function navButton(href, iconName, label, activeKey, pageKey, badge = '') {
  const isActive = activeKey === pageKey;
  const safeLabel = escapeHtml(label);
  return `<a class="nav-btn${isActive ? ' active' : ''}" href="${href}" title="${safeLabel}"${isActive ? ' aria-current="page"' : ''}>${icon(iconName)}<span class="sr-only">${safeLabel}</span>${badge}</a>`;
}

async function renderLayout() {
  const host = document.getElementById('site-header');
  if (!host) return;

  const inAdmin = location.pathname.includes('/admin/');
  const base = inAdmin ? '../' : '';
  const pageKey = currentPageKey();

  let session = { authenticated: false, user: null };
  try {
    session = (await apiRequest('/auth/session')).data;
  } catch (error) {
    /* API unreachable; render a signed-out header rather than blocking the page */
  }

  let unread = 0;
  if (session.authenticated) {
    try {
      unread = (await apiRequest('/notifications')).data.unread_count;
    } catch (error) {
      /* notifications are non-critical for the header */
    }
  }

  const links = [];
  if (session.authenticated) {
    links.push(navButton(`${base}dashboard.html`, 'home', 'Dashboard', pageKey, 'dashboard'));
    links.push(navButton(`${base}browse.html`, 'search', 'Browse', pageKey, 'browse'));
    links.push(navButton(`${base}messages.html`, 'chat', 'Messages', pageKey, 'messages'));
    links.push(navButton(`${base}notifications.html`, 'bell', 'Alerts', pageKey, 'notifications', unread ? `<span class="count">${unread}</span>` : ''));
    links.push(navButton(`${base}profile.html`, 'user', 'Profile', pageKey, 'profile'));
    if (session.user.role === 'ADMIN' || session.user.role === 'MODERATOR') {
      links.push(navButton(`${base}admin/dashboard.html`, 'shield', 'Admin', pageKey, 'admin-dashboard'));
    }
    links.push(`<button type="button" class="nav-btn" id="logout-link" title="Sign out">${icon('logout')}<span class="sr-only">Sign out</span></button>`);
  } else {
    links.push(navButton(`${base}browse.html`, 'search', 'Browse', pageKey, 'browse'));
    links.push(navButton(`${base}about.html`, 'info', 'About', pageKey, 'about'));
    links.push(navButton(`${base}login.html`, 'user', 'Sign in', pageKey, 'login'));
    links.push(navButton(`${base}register.html`, 'plus', 'Create account', pageKey, 'register'));
  }

  host.innerHTML = `
    <div class="bar">
      <a class="brand-btn" href="${base}index.html">${icon('home')}<span>Campus Lost &amp; Found</span></a>
      <nav>${links.join('')}</nav>
    </div>
  `;

  const logoutButton = document.getElementById('logout-link');
  if (logoutButton) {
    logoutButton.addEventListener('click', async () => {
      try {
        await apiRequest('/auth/logout', { method: 'POST' });
      } finally {
        window.location.href = `${base}index.html`;
      }
    });
  }

  return session;
}

const layoutReady = renderLayout();
