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