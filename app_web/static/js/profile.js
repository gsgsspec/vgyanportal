document.getElementById('save').onclick=function(){

    $('#profile_form').unbind('submit').bind('submit',function(event){
        event.preventDefault();

       
        dataObj = {
            'firstname': $('#firstname').val(),
            'lastname': $('#lastname').val(),
            'email': $('#email').val(),
            'password': $('#password').val(),
            'mbl_number': $('#mbl_number').val(),
            'address': $('#address').val(),
            'state': $('#state').val(),
            'country': $('#country').val(),
        }

        var form = $('#profile_form')[0];
        var data = new FormData(form);

        var fileInput = $('#upload')[0]; 
        data.append('file', fileInput.files[0]); 
        data.append('data',JSON.stringify(dataObj))
        data.append('csrfmiddlewaretoken',CSRF_TOKEN)



        $.ajax({
            type: "POST",
            enctype: 'multipart/form-data,application/json',
            url: CONFIG['domain'] + "/api/save-profile",
            data: data,
            processData: false,
            contentType: false,
            cache: false,
            timeout: 600000,
            success: function (res) {
                if(res.statusCode == 0){                  

                  showSuccessMessage('Profile details saved successfully')

                }else{
                  
                  showFailureMessage('Error in saving the profile details. Please try again after some time')

                  }
            }
        })

    })

}



document.addEventListener('DOMContentLoaded', function (e) {

    accountUserImage = document.getElementById('user_image');
    fileInput = document.querySelector('.account-file-input');

    if (accountUserImage) {
      resetImage = accountUserImage.src;
      fileInput.onchange = () => {
        if (fileInput.files[0]) {
          accountUserImage.src = window.URL.createObjectURL(fileInput.files[0]);
        }
      };
    }
});



