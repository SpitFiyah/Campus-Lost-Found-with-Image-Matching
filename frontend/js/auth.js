function showFormMessage(message, isError = true) {
  const element = document.querySelector('#form-message');
  element.textContent = message;
  element.className = isError ? 'alert alert-danger mt-3' : 'alert alert-success mt-3';
}

function bindAuthForm(formId, endpoint, redirectUrl) {
  document.querySelector(`#${formId}`).addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const formData = new FormData(form);
    const body = Object.fromEntries(formData.entries());
    try {
      await apiRequest(endpoint, { method: 'POST', body: JSON.stringify(body) });
      showFormMessage('Success. Redirecting...', false);
      window.location.href = redirectUrl;
    } catch (error) {
      showFormMessage(error.message);
    }
  });
}
