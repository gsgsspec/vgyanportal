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



function startAssessment(mid){
     
    dataObj = {
        'course_id': getUserCourseId,
        'module_id':mid,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'paper_title':paper_title+','+mid+')',
    }


    var final_data = {
        'data': JSON.stringify(dataObj),
        csrfmiddlewaretoken: CSRF_TOKEN,
    }

    $("#assessment_"+mid).html('')
    


    $.post(CONFIG['acert'] + "/api/vgyanportal-user-registeration", final_data, function (res) {

        if (res.statusCode == 0){

            $.post(CONFIG['domain'] + "/api/save-assessment", final_data, function (res) {
                if (res.statusCode == 0){

                    showSuccessMessage('Assessment requested successfully, please check your email')
                    
                }

                else {
                    showFailureMessage('Error in getting the assesment data. Please try after sometime')
                }

            })

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

    $('.lesson-icon').css("color", '');
    $('.lesson-title').css({"color":'',"text-decoration": "none"});


    $("#" + lid + " .lesson-icon").css("color", '#f46a24');
    $("#" + lid + " .lesson-title").css({
        "color": '#f46a24',
        "text-decoration": "underline"
    });

    $.post(CONFIG['domain'] + "/api/get-lesson-video", final_data, function (res) {

        if (res.statusCode == 0){

            video_id = res.data[0]
            library_id = res.data[1]
        
            $('#video_section').html('')

            $('#video_section').append(
                '<div style="position:relative;padding-top:56.25%">' +
                    '<iframe src="https://iframe.mediadelivery.net/embed/'+ library_id +'/'+ video_id +'?autoplay=true&loop=false&muted=false&preload=true" loading="lazy" ' +
                    'style="border:0;position:absolute;top:0;height:100%;width:100%;" allow="accelerometer;gyroscope;encrypted-media;picture-in-picture;" allowfullscreen="true"></iframe> ' +
                '</div>'
            )

        }


    })
    getVideoTime()
}


$(document).ready(function(){

    lesson_id = $(".list-group-item:first").attr("id")
    getCourseVideo(lesson_id)

    if (window.innerWidth > 900) {
        $('#layout-menu').css('display', 'none');
    }
    $('#web-page').removeClass('layout-menu-fixed')

    
    getVideoTime()
    

})

function getVideoTime(){
    console.log('1')
    video = document.getElementById('main-video');
    console.log('video-time ' ,video)
    setTimeout(getVideoTime, 1000);

}


function showFullPage(){

    $('#layout-menu').css('display','')
    $('#web-page').addClass('layout-menu-fixed')
    $('#display_icon').css('display','none')
    $('#hide_icon').css('display','block')

}


function hideFullPage(){
    $('#layout-menu').css('display','none')
    $('#web-page').removeClass('layout-menu-fixed')
    $('#display_icon').css('display','block')
    $('#hide_icon').css('display','none')
}


























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
    


$('#askQuestionId').click(function (){
    getAllQuestions()
})

function getAllQuestions(){
    var receivedData = localStorage.getItem('lessonId');
    var courseData = JSON.parse(receivedData)

    var lessonId  =  courseData

    dataObj = {
        'getQuestionData': lessonId
    }

    var final_data = {
        'data': JSON.stringify(dataObj),
        csrfmiddlewaretoken: CSRF_TOKEN,
    }

    $.post(CONFIG['domain'] + "/api/get-questions", final_data, function (res) {

        $('#courseId').html('')
        $('#moduleId').html('')
        $('#lessonId').html('')

        $('#courseId').text(res.data.courseDetails.courseGetName)
        $('#moduleId').text(res.data.courseDetails.courseModuleName)
        $('#lessonId').text(res.data.courseDetails.courseLessonName)

        var answeredQuestion = res.data.questionList;
        var overAllQuestions = res.data.overAllQuestions;
        
        var userRegIdentityId = res.data.sendUserId

        if (res.statusCode == 0) {

            $('#vertical-example').html('')
            $('#over-all-question').html('')


            for (var ans = 0; ans < overAllQuestions.length; ans++) {

                var question = overAllQuestions[ans]['ques'];
                var questionId = overAllQuestions[ans]['id'];
                var questionAnswer = overAllQuestions[ans]['ans'];
                var userRegisterationId = overAllQuestions[ans]['userId'];

                if (parseInt(userRegIdentityId) === userRegisterationId){

                    if (questionAnswer === 'N'){
                        var questionAnswerRes = "Not Answered"
                    }
                    else{
                        questionAnswerRes = questionAnswer
                    }

                    $('#vertical-example').append(
                        '<div class="accordion-item card m-2">' +
                        '<h2 class="accordion-header" id="headingOne' + questionId + '">' +
                        '<button type="button" class="accordion-button collapsed" data-bs-toggle="collapse" data-bs-target="#accordionOne' + questionId + '" aria-expanded="false" aria-controls="accordionOne' + questionId + '">' +
                        question + ' </button>' +
                        '</h2>' +
                        '<div id="accordionOne' + questionId + '" class="accordion-collapse collapse" data-bs-parent="#accordionExample">' +
                        '<div class="accordion-body"> ' + questionAnswerRes + ' </div>' +
                        '</div>' +
                        '</div>'
                    );

                }

                if (questionAnswer !== "N"){
                    $('#over-all-question').append(
                        '<div class="accordion-item card m-2">' +
                        '<h2 class="accordion-header " id="headingOne' + questionId + '">' +
                        '<button type="button" class="accordion-button collapsed" data-bs-toggle="collapse" data-bs-target="#accordionOne2' + questionId + '" aria-expanded="false" aria-controls="accordionOne' + questionId + '">' +
                        question + ' </button>' +
                        '</h2>' +
                        '<div id="accordionOne2' + questionId + '" class="accordion-collapse collapse" data-bs-parent="#accordionExample">' +
                        '<div class="accordion-body"> ' + questionAnswer + ' </div>' +
                        '</div>' +
                        '</div>'
                    );
                }

                

            }
        }
    });
}



function askQuestion(){

    $('#askQuestionForm').unbind('submit').bind('submit',function(event){
        event.preventDefault();

        var receivedData = localStorage.getItem('lessonId');
        var courseData = JSON.parse(receivedData)

        var lessonId  = courseData

        var question = $('#AskQuestionTextAreaId').val();

        dataObj = {
            'lessonId':  lessonId,
            'question':  question,
        }

        var final_data = {
            'data': JSON.stringify(dataObj),
            csrfmiddlewaretoken: CSRF_TOKEN,
        }

        $.post(CONFIG['domain'] + "/api/save-question", final_data, function (res) {
        
            if (res.statusCode == 0){
                showSuccessMessage('Question add') //success message

                $('#AskQuestionTextAreaId').val('');
                getAllQuestions()
            }
        })

    }) 
}