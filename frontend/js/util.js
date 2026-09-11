const HTML_ESCAPES = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, (char) => HTML_ESCAPES[char]);
}

function formatDate(value) {
  if (!value) return '';
  return new Date(value).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
}

function formatDateTime(value) {
  if (!value) return '';
  return new Date(value).toLocaleString(undefined, { year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
}

function imageUrl(imagePath) {
  return `${API_BASE_URL}/items/images/${encodeURIComponent(imagePath)}`;
}

function renderEmptyState(container, text) {
  container.innerHTML = `<div class="empty-state"><p>${escapeHtml(text)}</p></div>`;
}

function renderErrorState(container, message) {
  container.innerHTML = `<div class="error-state"><p>${escapeHtml(message)}</p></div>`;
}

function renderLoadingState(container, text = 'Loading…') {
  container.innerHTML = `<div class="loading-state"><p>${escapeHtml(text)}</p></div>`;
}

function typeBadge(type) {
  const cls = type === 'LOST' ? 'badge-lost' : 'badge-found';
  return `<span class="badge ${cls}">${escapeHtml(type)}</span>`;
}

function statusBadge(status) {
  const map = { ACTIVE: 'badge-neutral', MATCHED: 'badge-warning', RETURNED: 'badge-found', CLOSED: 'badge-neutral', REMOVED: 'badge-neutral' };
  return `<span class="badge ${map[status] || 'badge-neutral'}">${escapeHtml(status)}</span>`;
}

const ICONS = {
  home: '<polyline points="4 11 12 4 20 11"/><path d="M6 10v9a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1v-9"/>',
  search: '<circle cx="10" cy="10" r="6"/><line x1="20" y1="20" x2="14.5" y2="14.5"/>',
  chat: '<rect x="4" y="5" width="16" height="11" rx="2"/><polygon points="8,16 8,20 12,16"/>',
  bell: '<path d="M6 10a6 6 0 0 1 12 0v5l2 3H4l2-3z"/><path d="M10 21a2 2 0 0 0 4 0"/>',
  user: '<circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 4-6 8-6s8 2 8 6"/>',
  shield: '<path d="M12 3l7 3v6c0 5-3.5 8-7 9-3.5-1-7-4-7-9V6z"/>',
  logout: '<path d="M9 4H6a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h3"/><polyline points="15 16 20 12 15 8"/><line x1="20" y1="12" x2="9" y2="12"/>',
  back: '<line x1="20" y1="12" x2="4" y2="12"/><polyline points="10 6 4 12 10 18"/>',
  eye: '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
  edit: '<path d="M4 20l4-1 11-11-3-3L5 16z"/><line x1="14" y1="7" x2="17" y2="10"/>',
  plus: '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
  check: '<polyline points="4 12 10 18 20 6"/>',
  close: '<line x1="5" y1="5" x2="19" y2="19"/><line x1="19" y1="5" x2="5" y2="19"/>',
  flag: '<line x1="5" y1="3" x2="5" y2="21"/><path d="M5 4h14l-3 4 3 4H5"/>',
  send: '<polygon points="3 11 21 3 13 21 11 13 3 11"/>',
  save: '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="8" y="4" width="8" height="5"/>',
  photo: '<rect x="3" y="4" width="18" height="14" rx="2"/><circle cx="8" cy="9" r="1.5"/><polyline points="4 16 9 12 13 15 16 12 20 15"/>',
  gear: '<circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="8" stroke-dasharray="2 2"/>',
  undo: '<polyline points="9 10 4 15 9 20"/><path d="M20 4v7a4 4 0 0 1-4 4H4"/>',
  list: '<line x1="4" y1="6" x2="20" y2="6"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="18" x2="20" y2="18"/>',
  chart: '<line x1="4" y1="20" x2="4" y2="10"/><line x1="10" y1="20" x2="10" y2="4"/><line x1="16" y1="20" x2="16" y2="13"/>',
  info: '<circle cx="12" cy="12" r="9"/><line x1="12" y1="11" x2="12" y2="16"/><circle cx="12" cy="8" r="0.6" fill="currentColor" stroke="none"/>',
};

function icon(name, size = 18) {
  return `<svg class="icon" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[name] || ''}</svg>`;
}

// Static HTML can request an icon with <span data-icon="name"></span>
// instead of hand-writing inline SVG; this fills every occurrence in on load.
function hydrateIcons(root = document) {
  root.querySelectorAll('[data-icon]').forEach((el) => {
    el.innerHTML = icon(el.dataset.icon, Number(el.dataset.iconSize) || 18);
  });
}

document.addEventListener('DOMContentLoaded', () => hydrateIcons());
