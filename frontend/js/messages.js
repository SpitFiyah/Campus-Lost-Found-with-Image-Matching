function groupConversations(messages, myId) {
  const conversations = new Map();
  messages.forEach((message) => {
    const otherId = message.sender_id === myId ? message.receiver_id : message.sender_id;
    const otherName = message.sender_id === myId ? message.receiver_name : message.sender_name;
    const key = `${otherId}:${message.item_id || 'general'}`;
    if (!conversations.has(key)) {
      conversations.set(key, { otherId, otherName, itemId: message.item_id, itemName: message.item_name, messages: [] });
    }
    conversations.get(key).messages.push(message);
  });
  return Array.from(conversations.values()).sort((a, b) => new Date(b.messages.at(-1).created_at) - new Date(a.messages.at(-1).created_at));
}

async function loadMessages() {
  const container = document.querySelector('#list');
  const session = await layoutReady;
  const myId = session.user.id;
  const { data } = await apiRequest('/messages');

  if (data.messages.length === 0) {
    renderEmptyState(container, 'No messages yet. Start a conversation from an item page.');
    return;
  }

  const conversations = groupConversations(data.messages, myId);
  container.innerHTML = conversations.map((conversation) => `
    <article class="card">
      <h3>${escapeHtml(conversation.otherName || 'Unknown user')}${conversation.itemName ? ` <span class="muted">· ${escapeHtml(conversation.itemName)}</span>` : ''}</h3>
      <div class="stack">
        ${conversation.messages.map((message) => `
          <div>
            <p class="item-meta mt-0"><strong>${message.sender_id === myId ? 'You' : escapeHtml(message.sender_name)}</strong> · ${formatDateTime(message.created_at)}</p>
            <p>${escapeHtml(message.message)}</p>
          </div>
        `).join('')}
      </div>
      <form class="reply-form mt-4" data-receiver="${conversation.otherId}" data-item="${conversation.itemId || ''}">
        <div class="field mt-0">
          <textarea class="textarea" placeholder="Reply…" required></textarea>
        </div>
        <button class="btn btn-primary btn-sm" type="submit">${icon('send', 16)}Send</button>
      </form>
    </article>
  `).join('');

  container.querySelectorAll('.reply-form').forEach((form) => {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const textarea = form.querySelector('textarea');
      try {
        await apiRequest('/messages', {
          method: 'POST',
          body: JSON.stringify({
            receiver_id: Number(form.dataset.receiver),
            item_id: form.dataset.item ? Number(form.dataset.item) : null,
            message: textarea.value,
          }),
        });
        loadMessages();
      } catch (error) {
        renderErrorState(container, error.message);
      }
    });
  });
}

loadMessages().catch((error) => renderErrorState(document.querySelector('#list'), error.message));
