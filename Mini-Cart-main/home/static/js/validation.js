function checkWhitespace(value) {
  return value.trim() !== "";
}

const validateEmail = (email) => {
  return email.match(
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  );
};

const validatePassword = (password) => {
  return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(
    password
  );
};

function registerForm() {
  var fname = document.forms["myforms"]["fname"].value;
  var lname = document.forms["myforms"]["lname"].value;
  var email = document.forms["myforms"]["email"].value;
  var password = document.forms["myforms"]["password"].value;

  // Check for empty values
  if (!checkWhitespace(fname)) {
    alert("First Name cannot be empty");
    return false;
  }

  if (!checkWhitespace(lname)) {
    alert("Last Name cannot be empty");
    return false;
  }

  if (!checkWhitespace(email)) {
    alert("Email cannot be empty");
    return false;
  }

  if (!validateEmail(email)) {
    alert("Invalid Email Address");
    return false;
  }

  if (!checkWhitespace(password)) {
    alert("Password cannot be empty");
    return false;
  }

  if (!validatePassword(password)) {
    alert(
      "Password must contain at least one uppercase letter, one lowercase letter, one special character, one digit, and be at least 8 characters long"
    );
    return false;
  }

  return true;
}
