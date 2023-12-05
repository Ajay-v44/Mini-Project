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

//Register user

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

// Add Blogs

function blogForm() {
  var title = document.forms["blogform"]["title"].value;
  var description = document.forms["blogform"]["description"].value;
  if (!checkWhitespace(title)) {
    alert("Title cannot be empty");
    return false;
  }
  if (!checkWhitespace(description)) {
    alert("description  cannot be empty");
    return false;
  }

  return true;
}

// address form
function checkWhitespace(value) {
  return value.trim() !== "";
}

function addressForm() {
  var mob = document.forms["addressform"]["mob"].value;
  var expr = /^[6-9][0-9]{9}$/;
  if (isNaN(mob)) {
    alert("Mobile number must be a digit");
    return false;
  } else if (!expr.test(mob) || mob.length != 10) {
    alert("Invalid Phone Number");
    return false;
  } else {
    if (!checkWhitespace(mob)) {
      alert("Mobile cannot be empty");
      return false;
    }
  }

  var altermob = document.forms["addressform"]["altermob"].value;
  if (
    !checkWhitespace(altermob) ||
    isNaN(altermob) ||
    altermob.length !== 10 ||
    !expr.test(altermob)
  ) {
    alert("Invalid Alternate Number");
    return false;
  }
  var pincodeRegx = "^[1-9]{1}[0-9]{2}\\s{0, 1}[0-9]{3}$";
  var pincode = document.forms["addressform"]["pincode"].value;
  if (
    !checkWhitespace(pincode) ||
    isNaN(pincode) ||
    pincode.length !== 6 ||
    !pincodeRegx.test(pincode)
  ) {
    alert("Invalid Pincode");
    return false;
  }

  var address = document.forms["addressform"]["address"].value;
  if (!checkWhitespace(address) || address.length < 10) {
    alert("Invalid Address");
    return false;
  }

  return true;
}
