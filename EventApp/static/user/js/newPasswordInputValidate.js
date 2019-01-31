var userName = document.getElementById('userName');
var password1 = document.getElementById('password1');
var password2 = document.getElementById('password2');
var uname = 0, pass1 = 0, pass2 = 0;

function validateUserName() {
    if (userName.value == "") {
        document.getElementById("userNameErrors").style.display = "block";
        document.getElementById("userNameErrors").innerHTML = "Required";
        return false;
    }
    uname = 1;
    return true;
}

function validatePassword1() {

    if (password1.value == "") {
        document.getElementById("password1Errors").style.display = "block";
        document.getElementById("password1Errors").innerHTML = "Required";
        return false
    }
    pass1 = 1;
    return true;
}

function validatePassword2() {
    if (password2.value == "") {
        document.getElementById("password2Errors").style.display = "block";
        document.getElementById("password2Errors").innerHTML = "Required";
        return false
    }

    if (password1.value == password2.value) {
        pass2 = 1;
        return true;
    }
    else {
        document.getElementById("password2Errors").style.display = "block";
        document.getElementById("password2Errors").innerHTML = "Password fields do not match";
        return false;
    }
}


function validate() {
    clearFields();
    validateUserName();
    validatePassword1();
    validatePassword2();

    if (uname && pass1 && pass2) {
        return true;
    }
    else {
        return false;
    }
}

function clearFields() {
    document.getElementById("userNameErrors").innerHTML = "";
    document.getElementById("password1Errors").innerHTML = "";
    document.getElementById("password2Errors").innerHTML = "";
    document.getElementById("userNameErrors").style.display = "none";
    document.getElementById("password1Errors").style.display = "none";
    document.getElementById("password2Errors").style.display = "none";
}