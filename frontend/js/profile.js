async function loadProfile() {
  const container = document.querySelector('#profile');
  const { data } = await apiRequest('/auth/profile');
  const user = data.user;

  container.innerHTML = `
    <div class="row-between mt-0" style="padding-bottom: var(--space-4); margin-bottom: var(--space-4);">
      <div>
        <h1 class="mt-0">${escapeHtml(user.name)}</h1>
        <span class="badge badge-neutral">${escapeHtml(user.role)}</span>
      </div>
    </div>

    <div class="field"><span class="label">Email address</span><p>${escapeHtml(user.college_email)}</p></div>
    <div class="field"><span class="label">Student ID</span><p>${escapeHtml(user.student_id)}</p></div>
    <div class="field"><span class="label">Department</span><p>${escapeHtml(user.department)}</p></div>
    <div class="field"><span class="label">Phone</span><p>${user.phone ? escapeHtml(user.phone) : '<span class="muted">Not provided</span>'}</p></div>
    <div class="field"><span class="label">Account status</span><p>${user.is_verified ? 'Verified' : 'Pending verification'}</p></div>
    <div class="field"><span class="label">Member since</span><p>${formatDate(user.created_at)}</p></div>

    <a class="btn btn-outline" href="settings.html">${icon('gear')}Edit profile &amp; settings</a>
  `;
}

loadProfile().catch((error) => renderErrorState(document.querySelector('#profile'), error.message));
