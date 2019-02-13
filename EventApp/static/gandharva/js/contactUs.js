function SweetAlertSuccess() {
    swal({
        title: "Success!",
        text: "Message sent successfully",
        icon: "success",
        button: "Ok",
    });
}

function SweetAlertFailure() {
    swal({
        title: "Failure",
        text: "Message not sent",
        icon: "error",
        button: "Ok",
    });
}