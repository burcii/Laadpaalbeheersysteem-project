const API_BASE = 'http://127.0.0.1:8001';

const loginForm = document.querySelector('.login-form');
const registerForm = document.querySelector('.register-form');
const formTitle = document.querySelector('.form-title');

document.getElementById('showRegister').addEventListener('click', (e) => {
  e.preventDefault();
  loginForm.classList.remove('active');
  registerForm.classList.add('active');
  formTitle.textContent = 'Sign Up';
});

document.getElementById('showLogin').addEventListener('click', (e) => {
  e.preventDefault();
  registerForm.classList.remove('active');
  loginForm.classList.add('active');
  formTitle.textContent = 'Login';
});

const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirm-password');
const signUpBtn = document.getElementById('SignUpBtn');

function validatePassword() {
  if (password.value !== confirmPassword.value) {
    confirmPassword.setCustomValidity('Wachtwoorden komen niet overeen.');
  } else {
    confirmPassword.setCustomValidity('');
  }
}

password.addEventListener('change', validatePassword);
confirmPassword.addEventListener('change', validatePassword);

// ---------- LOGIN ----------
document.getElementById('SignInBtn').addEventListener('click', async (e) => {
  e.preventDefault();

  const email = document.getElementById('log-email').value.trim();
  const pass = document.getElementById('log-pass').value;

  if (!email && !pass) {
    return showPopupModel('Vul email en wachtwoord in');
  } else if (!email) {
    return showPopupModel('E-mailadres is verplicht.');
  } else if (!pass) {
    return showPopupModel('Wachtwoord is verplicht.');
  }

  try {
    const res = await fetch(`${API_BASE}/login?email=${encodeURIComponent(email)}&password=${encodeURIComponent(pass)}`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' }
    });

    const payload = await res.json();

    if (!res.ok) return showPopupModel(payload.error || 'Login mislukt');

    // store client-side
    localStorage.setItem('user_token', payload.token);

    // send token to PHP session
    const sessRes = await fetch('/set-session.php', {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: payload.token })
    });

    const sessJson = await sessRes.json().catch(() => ({}));
    if (!sessRes.ok) {
      console.error('set-session failed', sessRes.status, sessJson);
      return showPopupModel('Kon sessie niet instellen');
    }

    // success -> go to home
    window.location.href = '/';
  } catch (err) {
    console.error(err);
    showPopupModel('Netwerkfout tijdens inloggen');
  }
});

// ---------- REGISTER ----------
signUpBtn.addEventListener('click', async (e) => {
  e.preventDefault();
  validatePassword();

  if (password.value === '' || confirmPassword.value === '') {
    return showPopupModel('Vul een wachtwoord en bevestiging in');
  }
  if (password.value !== confirmPassword.value) {
    return showPopupModel('Wachtwoorden komen niet overeen.');
  }

  const countryCodeEl = document.getElementById('country-code');
  const phoneEl = document.getElementById('phone');
  const twofa = document.getElementById('twofa');

  const user = {
    firstName: document.getElementById('fname').value.trim() || '',
    lastName: document.getElementById('lname').value.trim() || '',
    email: document.getElementById('email').value.trim(),
    password: password.value,
    zipcode: document.getElementById('zip').value.trim() || '',
    country: document.getElementById('country').value || '',
    phonenumber: (countryCodeEl ? countryCodeEl.value : '') + (phoneEl ? phoneEl.value : ''),
    twofa: document.getElementById('twofa').value.trim() || ''
  };

  if (!user.email || !user.password) {
    return showPopupModel('Email en wachtwoord zijn verplicht');
  }

  try {
    const res = await fetch(`${API_BASE}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(user)
    });

    const data = await res.json();

    if (!res.ok) return showPopupModel(data.error || 'Registratie mislukt');

    showPopupModel(data.message || 'Registratie succesvol! Log in nu.');
    document.getElementById('showLogin').click();
  } catch (err) {
    console.error(err);
    showPopupModel('Netwerkfout tijdens registratie');
  }
});
