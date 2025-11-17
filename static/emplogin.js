document.addEventListener('DOMContentLoaded', () => {
  console.log("DOM fully loaded.");
  
  const form = document.getElementById('login-form');
  console.log("Found login form:", form);
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');
  const loginButton = document.getElementById('login-button');
  const errorMessage = document.getElementById('error-message');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log("Submit event triggered.");
    
    errorMessage.textContent = '';
    console.log("Cleared previous error messages.");

    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();
    console.log("Username after trim:", username);
    console.log("Password after trim:", password);

    if (!username || !password) {
      console.log("Error: Username or Password missing.");
      errorMessage.textContent = 'Username and Password are required.';
      return;
    }
    console.log("Username and password provided.");

    if (typeof grecaptcha === 'undefined') {
      console.log("Error: reCAPTCHA is undefined.");
      errorMessage.textContent = 'reCAPTCHA failed to load. Please refresh the page.';
      return;
    }
    console.log("reCAPTCHA exists.");

    const captchaToken = grecaptcha.getResponse();
    console.log("Captcha token received:", captchaToken);

    if (!captchaToken) {
      console.log("Error: Captcha token missing.");
      errorMessage.textContent = 'Please complete the CAPTCHA.';
      return;
    }
    console.log("Captcha token is valid.");

    loginButton.disabled = true;
    loginButton.textContent = 'Logging in...';
    console.log("Login button disabled, login in progress.");

    try {
      const response = await axios.post('/emplogin', {
        username,
        password,
        captchaToken
      });
      console.log("Server responded:", response);

      loginButton.disabled = false;
      loginButton.textContent = 'Login';
      console.log("Login button re-enabled.");

      if (response.status === 200) {
        console.log("Response status 200: Login successful.");
        alert(response.data.message);
        sessionStorage.setItem('user', response.data.username);
        console.log("User saved in sessionStorage:", response.data.username);

        if (response.data.designation === 'Admin') {
          console.log("User is an Admin. Redirecting to /admwelcome");
          window.location.href = '/admwelcome';
        } else {
          console.log("User is not an Admin. Redirecting to /empwelcome");
          window.location.href = '/empwelcome';
        }
      } else {
        console.log("Response status not 200, login failed.");
        errorMessage.textContent = response.data.message || 'Login failed. Please try again.';
      }
      console.log("Login attempt completed.");
    } catch (error) {
      console.error("Login Error caught:", error);
      loginButton.disabled = false;
      loginButton.textContent = 'Login';
      errorMessage.textContent = 'There was an error logging in. Please try again.';
    }
    
    console.log("Submit event handling finished.");
  });
});
