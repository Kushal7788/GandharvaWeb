var firstName = document.getElementById('firstName');
var lastName = document.getElementById('lastName');
var userName = document.getElementById('userName');
var EMail = document.getElementById('EMail');
var colEMail = document.getElementById('colEMail');
var password1 = document.getElementById('password1');
var password2 = document.getElementById('password2');
var mobile = document.getElementById('mobile');
var fname = 0, lname = 0, uname = 0, pass1 = 0, pass2 = 0, Email = 0, mob = 0, colemail = 0;

function validateFirstName() {
    var exp = /^[a-zA-Z]+$/;

    if (firstName.value == "") {
        document.getElementById("firstNameErrors").style.display = "block";
        document.getElementById("firstNameErrors").innerHTML = "Required";
        return false;
    }

    if (firstName.value.match(exp)) {
        fname = 1;
        return true;
    } else {
        document.getElementById("firstNameErrors").style.display = "block";
        document.getElementById("firstNameErrors").innerHTML = "Alphabets Only!";
        return false;
    }
}

function validateLastName() {
    var exp = /^[a-zA-Z]+$/;

    if (lastName.value == "") {
        document.getElementById("lastNameErrors").style.display = "block";
        document.getElementById("lastNameErrors").innerHTML = "Required";
        return false;
    }

    if (lastName.value.match(exp)) {
        lname = 1;
        return true;
    } else {
        document.getElementById("lastNameErrors").style.display = "block";
        document.getElementById("lastNameErrors").innerHTML = "Alphabets Only!";
        return false;
    }
}

function validateUserName() {
    if (userName.value == "") {
        document.getElementById("userNameErrors").style.display = "block";
        document.getElementById("userNameErrors").innerHTML = "Required";
        return false;
    }
    uname = 1;
    return true;
}


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

function validateColEMail() {
    var exp = /^([0-9a-zA-Z]([-.\w]*[0-9,a-zA-Z])*@([0-9a-zA-Z][-\w]*[0-9a-zA-Z]\.)+[a-zA-Z]{2,9})$/;

    if (colEMail.value == "") {
        document.getElementById("ColEmailErrors").style.display = "block";
        document.getElementById("ColEmailErrors").innerHTML = "Required";
        return false;
    }

    if (colEMail.value.match(exp)) {
        colemail = 1;
        return true;
    } else {
        document.getElementById("ColEmailErrors").style.display = "block";
        document.getElementById("ColEmailErrors").innerHTML = "Invalid Email";
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

function validateMobile() {
    var exp = /^[0-9]+$/;
    if (mobile.value == "") {
        document.getElementById("MobileErrors").style.display = "block";

        document.getElementById("MobileErrors").innerHTML = "Required";
        return false;
    }

    if (mobile.value.match(exp) && mobile.value.length == 10) {
        mob = 1;
        return true;
    } else {
        document.getElementById("MobileErrors").style.display = "block";
        document.getElementById("MobileErrors").innerHTML = "Invalid Number";
        return false;
    }

}

function validate() {
    clearFields();
    validateFirstName();
    validateLastName();
    validateUserName();
    validateEMail();
    validateColEMail();
    validatePassword1();
    validatePassword2();
    validateMobile();

    if (fname && lname && uname && pass1 && pass2 && Email && mob && colemail) {
        return true;
    }
    else {
        return false;
    }
}

function clearFields() {
    document.getElementById("firstNameErrors").innerHTML = "";
    document.getElementById("lastNameErrors").innerHTML = "";
    document.getElementById("userNameErrors").innerHTML = "";
    document.getElementById("EmailErrors").innerHTML = "";
    document.getElementById("ColEmailErrors").innerHTML = "";
    document.getElementById("password1Errors").innerHTML = "";
    document.getElementById("password2Errors").innerHTML = "";
    document.getElementById("MobileErrors").innerHTML = "";
    document.getElementById("firstNameErrors").style.display = "none";
    document.getElementById("lastNameErrors").style.display = "none";
    document.getElementById("userNameErrors").style.display = "none";
    document.getElementById("EmailErrors").style.display = "none";
    document.getElementById("ColEmailErrors").style.display = "none";
    document.getElementById("password1Errors").style.display = "none";
    document.getElementById("password2Errors").style.display = "none";
    document.getElementById("MobileErrors").style.display = "none";
}