<?php require __DIR__ . '/../components/popupModel/popupModel.php'; ?>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <title>Login / Registration</title>
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <link rel="stylesheet" href="styles/auth.css">
  <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
</head>

<body>
  <div class="wrapper">
    <div class="form-header">
      <div class="logo-container">
        <i class='bx bxs-bolt lightning-bolt'></i>
        <div class="form-title">Login</div>
      </div>
    </div>

    <!-- LOGIN FORM -->
    <form action="#" class="form login-form active" autocomplete="off">
      <div class="input-box">
        <input type="text" class="input-field" maxlength="50" id="log-email" required>
        <label for="log-email" class="label">Email</label>
        <i class='bx bx-envelope icon'></i>
      </div>
      <div class="input-box">
        <input type="password" class="input-field" id="log-pass" required>
        <label for="log-pass" class="label">Wachtwoord</label>
        <i class='bx bx-lock-alt icon'></i>
      </div>
      <div class="input-box">
        <button class="btn-submit" id="SignInBtn"><i class='bx bx-log-in'></i> Log in</button>
      </div>
      <div class="switch-form">
        <span>Geen account? <a href="#" id="showRegister">Sign Up!</a></span>
      </div>
    </form>

    <!-- REGISTER FORM -->
    <form action="#" class="form register-form" autocomplete="off">
      <div class="fname_lname">
        <div class="input-box">
          <input type="text" class="input-field" maxlength="16" id="fname" required>
          <label for="fname" class="label">Naam</label>
          <i class='bx bx-user icon'></i>
        </div>
        <div class="input-box">
          <input type="text" class="input-field" maxlength="16" id="lname" required>
          <label for="lname" class="label">Achternaam</label>
          <i class='bx bx-user icon'></i>
        </div>
      </div>

      <div class="input-box">
        <input type="email" class="input-field" maxlength="50" id="email" required>
        <label for="email" class="label">Email</label>
        <i class='bx bx-envelope icon'></i>
      </div>
      <div class="input-box">
        <input type="password" class="input-field" id="password" required>
        <label for="password" class="label">Wachtwoord</label>
        <i class='bx bx-lock-alt icon'></i>
      </div>

      <div class="input-box">
        <input type="password" class="input-field" id="confirm-password" required>
        <label for="confirm-password" class="label">Herhaal wachtwoord</label>
        <i class='bx bx-lock-alt icon'></i>
      </div>

      <div class="zselect">
        <div class="input-box">
          <input type="text" class="input-field" maxlength="8" id="zip" required>
          <label for="zip" class="label">Postcode</label>
        </div>
        <select class="form-select" id="country" name="country">
          <option>select country</option>
          <option value="AT">Austria</option>
          <option value="BE">Belgium</option>
          <option value="CA">Canada</option>
          <option value="CZ">Czech Republic</option>
          <option value="DK">Denmark</option>
          <option value="FI">Finland</option>
          <option value="FR">France</option>
          <option value="DE">Germany</option>
          <option value="IE">Ireland</option>
          <option value="IT">Italy</option>
          <option value="LU">Luxembourg</option>
          <option value="NL">Netherlands</option>
          <option value="NO">Norway</option>
          <option value="ES">Spain</option>
          <option value="SE">Sweden</option>
          <option value="CH">Switzerland</option>
          <option value="GB">United Kingdom</option>
          <option value="US">United States</option>
        </select>
      </div>

      <div class="input-box">
        <select id="country-code" class="form-select" required>
          <option value="+31">+31 (NL)</option>
          <option value="+32">+32 (BE)</option>
          <option value="+44">+44 (UK)</option>
          <option value="+1">+1 (US)</option>
          <option value="+49">+49 (DE)</option>
          <!--Add more if u want -->
        </select>
        <input type="tel" id="phone" class="input-field" placeholder="612345678" required>
        <i class='bx bx-phone icon'></i>
      </div>

      <div class="input-box">
        <input type="text" class="input-field" id="twofa" />
        <label for="2fa" class="label">Admin Code (Not Required)</label>
        <i class='bx bx-lock-alt icon'></i>
      </div>

      <div class="input-box">
        <button class="btn-submit" id="SignUpBtn">Sign Up! <i class='bx bx-right-arrow-alt'></i></button>
      </div>
      <div class="switch-form">
        <span>Al een account? <a href="#" id="showLogin">Log in!</a></span>
      </div>
    </form>
  </div>

  <script src="services/auth.js"></script>
</body>

</html>