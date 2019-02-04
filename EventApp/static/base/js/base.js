$(document).ready(function () {
    // Transition effect for navbar
    $(window).scroll(function () {
        // checks if window is scrolled more than 500px, adds/removes solid class
        if ($(this).scrollTop() > 200) {
            $('.navbar').addClass('solid');
            $('.navbar').css("background-color: #004E8A;");
        } else {
            $('.navbar').removeClass('solid');
        }
    });
});


function goToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}
