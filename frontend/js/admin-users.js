renderAdminNav('users');

async function loadUsers() {
  const container = document.querySelector('#list');
  const { data } = await apiRequest('/admin/users');

  if (data.users.length === 0) {
    renderEmptyState(container, 'No users yet.');
    return;
  }

  container.innerHTML = `
    <div class="table-wrap"><table>
      <thead><tr><th>Name</th><th>College email</th><th>Student ID</th><th>Department</th><th>Role</th><th>Verified</th><th>Joined</th></tr></thead>
      <tbody>
        ${data.users.map((user) => `
          <tr>
            <td>${escapeHtml(user.name)}</td>
            <td>${escapeHtml(user.college_email)}</td>
            <td>${escapeHtml(user.student_id)}</td>
            <td>${escapeHtml(user.department)}</td>
            <td>${escapeHtml(user.role)}</td>
            <td>${user.is_verified ? 'Yes' : 'No'}</td>
            <td>${formatDate(user.created_at)}</td>
          </tr>
        `).join('')}
      </tbody>
    </table></div>
  `;
}

loadUsers().catch((error) => renderErrorState(document.querySelector('#list'), error.message));
