async function login() {
  const form = document.getElementById("loginAdmin");
  const formData = new FormData(form);

  const response = await fetch(`http://localhost:5000/login`, {
    method: 'POST',
    body: formData
  });

  if (response.ok) {
    const data = await response.json();
    sessionStorage.setItem('access_token', data.access_token);
    window.location.href = "./admin.html";
  } else {
    throw new Error('Failed to login');
  }
}

async function submitLogin() {
  await login()
}