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

localStorage.removeItem('dataObj');



document.getElementById('courseDetailsData').onclick=function(){

    dataObj = {
        'courseId'  : getUserCourseId,
    }
    localStorage.setItem('dataObj', JSON.stringify(dataObj));

    window.location.href = '/ask-question';
}

$('#startAssessment').click( function(){

    console.log('Start Assessment :: ',dataObj)

} )




































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
    
