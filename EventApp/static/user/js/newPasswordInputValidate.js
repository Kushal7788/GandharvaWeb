var EMail = document.getElementById('EMail');
var password1 = document.getElementById('password1');
var password2 = document.getElementById('password2');
var Email = 0, pass1 = 0, pass2 = 0;

function validateEMail() {
    var exp = /^([0-9a-zA-Z]([-.\w]*[0-9,a-zA-Z])*@([0-9a-zA-Z][-\w]*[0-9a-zA-Z]\.)+[a-zA-Z]{2,9})$/;

    if (EMail.value == "") {
        document.getElementById("EmailErrors").style.display = "block";
        document.getElementById("EmailErrors").innerHTML = "Required";
        return false;
    }

    if (EMail.value.match(exp)) {
        Email = 1;
        return true;
    } else {
        document.getElementById("EmailErrors").style.display = "block";
        document.getElementById("EmailErrors").innerHTML = "Invalid Email";
        return false;
    }
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
    validateEMail();
    validatePassword1();
    validatePassword2();

    if (Email && pass1 && pass2) {
        return true;
    }
    else {
        return false;
    }
}

function clearFields() {
    document.getElementById("EmailErrors").innerHTML = "";
    document.getElementById("password1Errors").innerHTML = "";
    document.getElementById("password2Errors").innerHTML = "";
    document.getElementById("EmailErrors").style.display = "none";
    document.getElementById("password1Errors").style.display = "none";
    document.getElementById("password2Errors").style.display = "none";
}