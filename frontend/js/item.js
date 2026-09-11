const itemId = new URLSearchParams(location.search).get('id');

function renderImages(images) {
  if (images.length === 0) return '';
  return `<div class="item-grid" style="grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); margin-bottom: var(--space-4);">
    ${images.map((image) => `<img class="item-thumb" src="${imageUrl(image.image_path)}" alt="Photo">`).join('')}
  </div>`;
}

function renderOwnerActions(item) {
  return `
    <div class="row mt-4">
      <a class="btn btn-primary" href="matches.html?id=${item.id}">${icon('check')}View possible matches</a>
      <button class="btn btn-outline" id="edit-toggle" type="button">${icon('edit')}Edit report</button>
    </div>
    <form id="edit-form" class="card mt-4 hidden">
      <div class="field-row">
        <div class="field"><label for="edit-name">Name</label><input class="input" id="edit-name" value="${escapeHtml(item.name)}"></div>
        <div class="field"><label for="edit-category">Category</label><input class="input" id="edit-category" value="${escapeHtml(item.category)}"></div>
      </div>
      <div class="field"><label for="edit-description">Description</label><textarea class="textarea" id="edit-description">${escapeHtml(item.description)}</textarea></div>
      <div class="field-row">
        <div class="field"><label for="edit-color">Color</label><input class="input" id="edit-color" value="${escapeHtml(item.color || '')}"></div>
        <div class="field"><label for="edit-location">Location</label><input class="input" id="edit-location" value="${escapeHtml(item.location)}"></div>
      </div>
      <button class="btn btn-primary" type="submit">${icon('save')}Save changes</button>
      <p id="edit-message" class="mt-4"></p>
    </form>
  `;
}

function renderContactActions(item) {
  return `
    <form id="message-form" class="card mt-4">
      <h3>Message the reporter</h3>
      <div class="field">
        <label for="message-text">Your message</label>
        <textarea class="textarea" id="message-text" placeholder="Ask about a detail only the owner would know before arranging a meetup." required></textarea>
      </div>
      <button class="btn btn-primary" type="submit">${icon('send')}Send message</button>
      <p id="message-status" class="mt-4"></p>
    </form>
    <details class="card mt-4">
      <summary style="cursor: pointer; font-weight: 700;">${icon('flag')}Flag this report</summary>
      <form id="report-form" class="mt-4">
        <div class="field">
          <label for="report-reason">Reason</label>
          <select class="select" id="report-reason" required>
            <option value="">Choose a reason</option>
            <option>Spam or irrelevant</option>
            <option>Suspected fraud</option>
            <option>Duplicate report</option>
            <option>Inappropriate content</option>
            <option>Other</option>
          </select>
        </div>
        <div class="field">
          <label for="report-description">Details (optional)</label>
          <textarea class="textarea" id="report-description"></textarea>
        </div>
        <button class="btn btn-outline" type="submit">${icon('flag')}Submit flag</button>
        <p id="report-status" class="mt-4"></p>
      </form>
    </details>
  `;
}

async function loadItem() {
  const container = document.querySelector('#detail');
  const session = await layoutReady;
  const { data } = await apiRequest(`/items/${itemId}`);
  const item = data.item;
  const isOwner = session && session.authenticated && session.user.id === item.user_id;

  container.innerHTML = `
    ${renderImages(item.images)}
    <div class="row">${typeBadge(item.type)} ${statusBadge(item.status)}</div>
    <h1 class="mt-4">${escapeHtml(item.name)}</h1>
    <p class="lead">${escapeHtml(item.description)}</p>
    <p class="item-meta">${escapeHtml(item.category)} · ${escapeHtml(item.color || 'Color not specified')} · ${escapeHtml(item.location)} · ${formatDate(item.date_lost_found)}</p>
    ${isOwner ? renderOwnerActions(item) : (session && session.authenticated ? renderContactActions(item) : `<a class="btn btn-outline mt-4" href="login.html">${icon('user')}Sign in to message the reporter or flag this report</a>`)}
  `;

  if (isOwner) {
    document.querySelector('#edit-toggle').addEventListener('click', () => {
      document.querySelector('#edit-form').classList.toggle('hidden');
    });
    document.querySelector('#edit-form').addEventListener('submit', async (event) => {
      event.preventDefault();
      const form = new FormData();
      form.set('name', document.querySelector('#edit-name').value);
      form.set('category', document.querySelector('#edit-category').value);
      form.set('description', document.querySelector('#edit-description').value);
      form.set('color', document.querySelector('#edit-color').value);
      form.set('location', document.querySelector('#edit-location').value);
      const status = document.querySelector('#edit-message');
      try {
        await apiRequest(`/items/${item.id}`, { method: 'PUT', body: form });
        status.textContent = 'Saved.';
        loadItem();
      } catch (error) {
        status.textContent = error.message;
      }
    });
    return;
  }

  if (!session || !session.authenticated) return;

  document.querySelector('#message-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const status = document.querySelector('#message-status');
    try {
      await apiRequest('/messages', {
        method: 'POST',
        body: JSON.stringify({ item_id: item.id, receiver_id: item.user_id, message: document.querySelector('#message-text').value }),
      });
      status.textContent = 'Message sent.';
      event.target.reset();
    } catch (error) {
      status.textContent = error.message;
    }
  });

  document.querySelector('#report-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const status = document.querySelector('#report-status');
    try {
      await apiRequest(`/items/${item.id}/report`, {
        method: 'POST',
        body: JSON.stringify({ reason: document.querySelector('#report-reason').value, description: document.querySelector('#report-description').value }),
      });
      status.textContent = 'Thanks, this report has been flagged for review.';
      event.target.reset();
    } catch (error) {
      status.textContent = error.message;
    }
  });
}

loadItem().catch((error) => renderErrorState(document.querySelector('#detail'), error.message));
