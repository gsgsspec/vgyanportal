document.getElementById('login').onclick=function(){

    $('#login_form').unbind('submit').bind('submit',function(event){
        event.preventDefault();

       
        dataObj = {
            'email': $('#email').val(),
            'password': $('#password').val(),
        }

        var final_data = {
            'data': JSON.stringify(dataObj),
            csrfmiddlewaretoken: CSRF_TOKEN,
        }

        $.post(CONFIG['domain'] + "/api/login", final_data, function (res) {
            console.log('res',res);
        
            if (res.statusCode == 0){
                if (res.token == 'token_generated'){
                    window.location.href = '/courses';
                }
                else{
                    $('#invalid_cred').removeAttr('hidden');
                }
            }

        })
    })

}