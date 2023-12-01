function showSuccessMessage(message) {
    $('.bs-toast.toast.bg-success').removeAttr('hidden');
    $('.bs-toast.toast.bg-success .toast-body').text(message);
    $('.bs-toast.toast.bg-success').toast('show');
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

}

    

