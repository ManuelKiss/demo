const form = document.getElementById('login-form');
const accountInput = document.getElementById('account');
const passwordInput = document.getElementById('password');
const accountError = document.getElementById('account-error');
const passwordError = document.getElementById('password-error');
const toggleButton = document.getElementById('toggle-password');
const submitButton = document.getElementById('submit-button');

const INVALID_CLASS = 'login-form__input--invalid';
const SHOW_CLASS = 'login-form__error--show';

const setError = (input, messageEl, show) => {
  input.classList.toggle(INVALID_CLASS, show);
  messageEl.classList.toggle(SHOW_CLASS, show);
};

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const handleTogglePassword = () => {
  passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
};

const handleSubmit = async (event) => {
  event.preventDefault();

  const accountInvalid = accountInput.value.trim() === '';
  const passwordInvalid = passwordInput.value.length < 6;
  setError(accountInput, accountError, accountInvalid);
  setError(passwordInput, passwordError, passwordInvalid);
  if (accountInvalid || passwordInvalid) {
    return;
  }

  submitButton.disabled = true;
  submitButton.textContent = '登录中…';
  try {
    // 模拟登录请求，实际项目中替换为 await fetch('/api/login', ...)
    await delay(1200);
    window.alert('登录成功（演示）');
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = '登 录';
  }
};

const clearErrorOnInput = (input, messageEl) => {
  input.addEventListener('input', () => setError(input, messageEl, false));
};

toggleButton.addEventListener('click', handleTogglePassword);
form.addEventListener('submit', handleSubmit);
clearErrorOnInput(accountInput, accountError);
clearErrorOnInput(passwordInput, passwordError);
