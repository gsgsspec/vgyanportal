document.getElementById('save_rating').onclick=function(){

    $('#rating_form').unbind('submit').bind('submit',function(event){
        event.preventDefault();
       
        dataObj = {
            'rating':  $('input[name=rating_star]:checked').val(),
            'comments': $('#rating_comment').val(),
            'course_id': $('#courseid').attr('name'),
        }

        var final_data = {
            'data': JSON.stringify(dataObj),
            csrfmiddlewaretoken: CSRF_TOKEN,
        }

        $.post(CONFIG['domain'] + "/api/save-rating", final_data, function (res) {
        
            if (res.statusCode == 0){
                rating = res.data

                showSuccessMessage('Thanks for your feedback')
                $('#rating_button').hide();
                $('#user-rating').append('<p style="font-size:1.125rem">Rating : ' + rating + ' <i class="fas fa-star" style="color: #f46a24;"></i></p>');
                $('#user-rating').removeAttr('hidden');
                $('#rating_popup').modal('hide');
            }
            else {
                showFailureMessage('Error in saving course rating. Please try again after some time')
            }
        })
    })

}



document.getElementById('courseDetailsData').onclick=function(){
  
    window.location.href = '/course/question';
}



function startAssessment(mid){
     
    dataObj = {
        'course_id': getUserCourseId,
        'module_id':mid,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'paper_id' : '1',
    }


    var final_data = {
        'data': JSON.stringify(dataObj),
        csrfmiddlewaretoken: CSRF_TOKEN,
    }

    $.post(CONFIG['acert'] + "/api/vgyanportal-user-registeration", final_data, function (res) {

        if (res.statusCode == 0){

            showSuccessMessage('Please check your mail for the assessment details')
        }

        else {
            showFailureMessage('Error in getting the assesment data. Please try after sometime')
        }

    })
    
}



function getCourseVideo(lid){

    dataObj ={
        'lesson_id':lid
    }

    // local storage lession id
    localStorage.setItem('lessonId',JSON.stringify(dataObj))

    var final_data = {
        'data': JSON.stringify(dataObj),
        csrfmiddlewaretoken: CSRF_TOKEN,
    }

    $.post(CONFIG['domain'] + "/api/get-lesson-video", final_data, function (res) {

        if (res.statusCode == 0){

            video_id = res.data[0]
            library_id = res.data[1]
        
            $('#video_section').html('')

            $('#video_section').append(
                '<div style="position:relative;padding-top:56.25%;">' +
                    '<iframe src="https://iframe.mediadelivery.net/embed/'+ library_id +'/'+ video_id +'?autoplay=true&loop=false&muted=false&preload=true" loading="lazy" ' +
                    'style="border:0;position:absolute;top:0;height:100%;width:100%;" allow="accelerometer;gyroscope;encrypted-media;picture-in-picture;" allowfullscreen="true"></iframe> ' +
                '</div>'
            )

        }


    })
}


$(document).ready(function(){

    lesson_id = $(".list-group-item:first").attr("id")
    getCourseVideo(lesson_id)

})
































$(document).on({
    mouseover: function(event) {
        $(this).find('.far').addClass('star-over');
        $(this).prevAll().find('.far').addClass('star-over');
    },
    mouseleave: function(event) {
        $(this).find('.far').removeClass('star-over');
        $(this).prevAll().find('.far').removeClass('star-over');
    }
}, '.rate');


$(document).on('click', '.rate', function() {
    if ( !$(this).find('.star').hasClass('rate-active') ) {
        $(this).siblings().find('.star').addClass('far').removeClass('fas rate-active');
        $(this).find('.star').addClass('rate-active fas').removeClass('far star-over');
        $(this).prevAll().find('.star').addClass('fas').removeClass('far star-over');
    } else {
        console.log('has');
    }
});
    
