const viewedItemId = Number(new URLSearchParams(location.search).get('id')) || null;

function renderMatchCard(match, other) {
  const thumb = other.images[0] ? `<img class="item-thumb" src="${imageUrl(other.images[0].image_path)}" alt="Photo of ${escapeHtml(other.name)}" style="max-width: 140px;">` : '';
  const actions = match.status === 'PENDING'
    ? `<button class="btn btn-primary btn-sm" data-action="accept" data-id="${match.id}">${icon('check', 16)}Accept</button>
       <button class="btn btn-outline btn-sm" data-action="reject" data-id="${match.id}">${icon('close', 16)}Reject</button>`
    : match.status === 'ACCEPTED'
      ? `<button class="btn btn-outline btn-sm" data-action="returned" data-id="${match.id}">${icon('undo', 16)}Mark as returned</button>`
      : '';
  return `
    <article class="card row">
      ${thumb}
      <div style="flex: 1;">
        <div>${statusBadge(match.status)}</div>
        <h3>${escapeHtml(other.name)}</h3>
        <p class="item-meta">${escapeHtml(other.location)} · ${formatDate(other.date_lost_found)}</p>
        <p class="item-meta">Match score: ${Math.round(match.final_score)}%</p>
        <a class="btn btn-outline btn-sm" href="item.html?id=${other.id}">${icon('eye', 16)}View item</a>
        <div class="row mt-4">${actions}</div>
      </div>
    </article>
  `;
}

function bindActions(container, reload) {
  container.querySelectorAll('button[data-action]').forEach((button) => {
    button.addEventListener('click', async () => {
      button.disabled = true;
      try {
        const path = button.dataset.action === 'returned' ? `/matches/${button.dataset.id}/returned` : `/matches/${button.dataset.id}/${button.dataset.action}`;
        await apiRequest(path, { method: 'POST' });
        reload();
      } catch (error) {
        renderErrorState(container, error.message);
      }
    });
  });
}

async function loadItemMatches() {
  const container = document.querySelector('#list');
  const { data } = await apiRequest(`/items/${viewedItemId}/matches`);
  if (data.matches.length === 0) {
    renderEmptyState(container, "No potential matches yet. We'll show new ones here as they're found.");
    return;
  }
  container.innerHTML = data.matches.map((match) => renderMatchCard(match, match.lost_item_id === viewedItemId ? match.found_item : match.lost_item)).join('');
  bindActions(container, loadItemMatches);
}

async function loadMyMatches() {
  const container = document.querySelector('#list');
  const session = await layoutReady;
  const { data } = await apiRequest('/matches');
  if (data.matches.length === 0) {
    renderEmptyState(container, "No potential matches yet across your reports.");
    return;
  }
  container.innerHTML = data.matches.map((match) => renderMatchCard(match, match.lost_item.user_id === session.user.id ? match.found_item : match.lost_item)).join('');
  bindActions(container, loadMyMatches);
}

const load = viewedItemId ? loadItemMatches : loadMyMatches;
load().catch((error) => renderErrorState(document.querySelector('#list'), error.message));
