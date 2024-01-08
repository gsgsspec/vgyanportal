function showSuccessMessage(message) {

    $('.bs-toast.toast.bg-success').removeAttr('hidden');
    $('.bs-toast.toast.bg-success .toast-body').text(message);
    $('.bs-toast.toast.bg-success').toast('show');
    $('.bs-toast.toast.bg-success .toast-timeout').css('width', '100%');

    setTimeout(function() {
        $('.bs-toast.toast.bg-success .toast-timeout').css('width', '');
    }, 5200);
}

function showFailureMessage(message) {

    $('.bs-toast.toast.bg-danger').removeAttr('hidden');
    $('.bs-toast.toast.bg-danger .toast-body').text(message);
    $('.bs-toast.toast.bg-danger').toast('show');
}


$(document).ready(menu_bar)

function menu_bar() {
    var current_url = window.location.href


    if (current_url.includes('profile')){
        $('.menu-item:has(a[href="/profile"])').addClass('active');
    }

    if (current_url.includes('course')){
        $('.menu-item:has(a[href="/courses"])').addClass('active');
    }

    if (current_url.includes('assessments')){
        $('.menu-item:has(a[href="/assessments"])').addClass('active');
    }

}


document.addEventListener('DOMContentLoaded', () => {
    const loader = document.getElementById('loader');

    window.addEventListener('load', () => {
        loader.style.display = 'none';
    });
});



    

