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



function startAssessment(mid, buttonDiv){
     
    dataObj = {
        'course_id': getUserCourseId,
        'module_id':mid,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'paper_title':paper_title+','+mid+')',
    }

    buttonDiv.disabled=true


    var final_data = {
        'data': JSON.stringify(dataObj),
        csrfmiddlewaretoken: CSRF_TOKEN,
    }

    
    $.post(CONFIG['acert'] + "/api/vgyanportal-user-registeration", final_data, function (res) {

        if (res.statusCode == 0){

            $.post(CONFIG['domain'] + "/api/save-assessment", final_data, function (res) {
                if (res.statusCode == 0){

                    $("#assessment_"+mid).html('')
                    $("#assessment_"+mid).removeClass('justify-content-end')
                    $("#assessment_"+mid).append('<p><i class="fas fa-check-circle" style="color:#71dd37"></i>&ensp;Assessment requested successfully please check your email.</p>')
                    
                }

                else {
                    showFailureMessage('Error in getting the assesment data. Please try after sometime')
                    buttonDiv.disabled=false
                    
                }

            })

        }

        else {
            showFailureMessage('Error in getting the assesment data. Please try after sometime')
            buttonDiv.disabled=false
        }

    }).fail(function (){
        showFailureMessage('Error in getting the assesment data. Please try after sometime')
            buttonDiv.disabled=false
    })

    
}


function getCourseVideo(lid){

    getLesssonData(lid)

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

    playing_lesson_id = lid

    saveVideoActivity(lid)

    $.post(CONFIG['domain'] + "/api/get-lesson-video", final_data, function (res) {

        if (res.statusCode == 0){

            video_id = res.data[0]
            library_id = res.data[1]
            video_time = res.data[2]

            video_src = "https://"+ library_id +"/"+video_id+"/play_720p.mp4#t="+ video_time +""
            $('#video-src').attr('src',video_src)

        }
        
    })  
}

let watched_lesson_id = null;
let playing_lesson_id = null;

function saveVideoActivity(lid){


    if(!watched_lesson_id){
        watched_lesson_id = lid     
    }  

    else{

        video = document.getElementById('video-src')
        video_time = video.currentTime

        dataObj ={
            'lesson_id':watched_lesson_id,
            'time_duration': video_time,
            'current_video_id':lid
        }
    
        var final_data = {
            'data': JSON.stringify(dataObj),
            csrfmiddlewaretoken: CSRF_TOKEN,
        }

        $.post(CONFIG['domain'] + "/api/save-video-activity", final_data, function (res) {
            if (res.statusCode == 0){
                watched_lesson_id = lid
            }
    
        })
    }
   
}


$(document).ready(function(){

    checkLatestNotifications() // Check Latest Notification function Calling

    if (current_lessonid == 'None'){
        lesson_id = $(".list-group-item:first").attr("id")
    }
    else{
        lesson_id = current_lessonid
    }
    

    getCourseVideo(lesson_id)
    activeVideoAccordian(lesson_id)

    if (window.innerWidth > 900) {
        $('#layout-menu').css('display', 'none');
    }
    $('#web-page').removeClass('layout-menu-fixed')


    playPauseButton = document.querySelector('.play-pause');
    if (playPauseButton){
        playPauseButton.addEventListener('click', function() {

            var playing_lesson = playing_lesson_id
            saveVideoActivity(playing_lesson)

        })
    }

})



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
    

function activeVideoAccordian(lesson_id){
    var accordionItem = $('#'+lesson_id).closest('.accordion-item').find('.accordion-button');
    accordionItem.click()
}


function getLesssonData(lesson_id){

   lesson_title =  $('#'+lesson_id).find('.lesson-title').text();
   $('h5[data-lesson-name="lesson-name"]').text(lesson_title);

}

function updateLessonstatus(lesson_id){

    var status_checkbox = document.getElementById('lesson_check_'+lesson_id)
    var lesson_status = status_checkbox.checked ? 'C' : 'N';
    

    dataObj = {
        'lesson_id':lesson_id,
        'lesson_status':lesson_status
    }

    var final_data = {
        'data': JSON.stringify(dataObj),
        csrfmiddlewaretoken: CSRF_TOKEN,
    }

    $.post(CONFIG['domain'] + "/api/update-lesson-status", final_data, function (res) {
        if (res.statusCode == 0){
            watched_lesson_id = lid
        }

    })
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

$('#MobileaskQuestionId').click(function (){
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
        console.log('overAllQuestions :: ',overAllQuestions)
        var userRegIdentityId = res.data.sendUserId

        if (res.statusCode == 0) {

            $('#vertical-example').html('')
            $('#over-all-question').html('')


            for (var ans = 0; ans < overAllQuestions.length; ans++) {

                var question = overAllQuestions[ans]['ques'];
                var questionId = overAllQuestions[ans]['id'];
                var questionAnswer = overAllQuestions[ans]['ans'];
                var questionDate = overAllQuestions[ans]['queDate']
                var questionTime = overAllQuestions[ans]['queTime']
                var userRegisterationId = overAllQuestions[ans]['userId'];

                if (parseInt(userRegIdentityId) === parseInt(userRegisterationId)){

                    if (questionAnswer === 'N'){
                        var questionAnswerRes = "Not Answered"
                    }
                    else{
                        questionAnswerRes = questionAnswer
                    }

                    $('#vertical-example').append(
                        '<div class="accordion-item card m-2">' +
                        '<h2 class="accordion-header" id="verticalHeading' + questionId + '">' +
                        '<button type="button" class="accordion-button collapsed accordian-cust-sm-cls" data-bs-toggle="collapse" data-bs-target="#verticalAccordion' + questionId + '" aria-expanded="false" aria-controls="verticalAccordion' + questionId + '">' +
                        '<div style="display: flex; justify-content: center;"> <p class="p-0 m-0 time-container" style="font-size: 12px; color: var(--bs-body-color);width:69px;"> <i class="fas fa-clock clock-icon-cls" style="color: #f46a24 !important;"></i> <span id="hidde-clock-in-mobile">  '+ questionTime +' </span>'  + questionDate +' </p> <div class="vr vr-rm-sm" style="background-color: #f46a24; width:2px; margin: 0rem 0.5rem;"></div></div>' + question + ' </button> ' +
                        '</h2>' +
                        '<div id="verticalAccordion' + questionId + '" class="accordion-collapse collapse" aria-labelledby="verticalHeading' + questionId + '" data-bs-parent="#vertical-example">' +
                        '<div class="accordion-body"> ' + questionAnswerRes + ' </div>' +
                        '</div>' +
                        '</div>'
                    );
                    
                }

                $('#over-all-question').append(
                    '<div class="accordion-item2 card m-2">' +
                    '<h2 class="accordion-header" id="overallHeading' + questionId + '">' +
                    '<button type="button" class="accordion-button collapsed accordian-cust-sm-cls" data-bs-toggle="collapse" data-bs-target="#overallAccordion' + questionId + '" aria-expanded="false" aria-controls="overallAccordion' + questionId + '">' +
                    '<div style="display: flex; justify-content: center;"> <p class="p-0 m-0 time-container" style="font-size: 12px; color: var(--bs-body-color);width:69px;"> <i class="fas fa-clock clock-icon-cls" style="color: #f46a24 !important;"></i> <span id="hidde-clock-in-mobile">  '+ questionTime +' </span>'  + questionDate +' </p> <div class="vr vr-rm-sm" style="background-color: #f46a24; width:2px; margin: 0rem 0.5rem;"></div></div>' + question + ' </button> ' +
                    '</h2>' +
                    '<div id="overallAccordion' + questionId + '" class="accordion-collapse collapse" aria-labelledby="overallHeading' + questionId + '" data-bs-parent="#over-all-question">' +
                    '<div class="accordion-body"> ' + questionAnswerRes + ' </div>' +
                    '</div>' +
                    '</div>'
                );

                

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
        var videoCurrentVideoTime = document.getElementById('video-src')

        var videotime = videoCurrentVideoTime.currentTime
        var vidTime =  videotime

        var question = $('#AskQuestionTextAreaId').val();   

        console.log('videoCurrentVideoTime',)

        dataObj = {
            'lessonId':  lessonId,
            'question':  question,
           'videotimecurr':  vidTime 
        }

        var final_data = {
            'data': JSON.stringify(dataObj),
            csrfmiddlewaretoken: CSRF_TOKEN,
        }

        $.post(CONFIG['domain'] + "/api/save-question", final_data, function (res) {
        
            if (res.statusCode == 0){
                showSuccessMessage('Question added') //success message

                $('#AskQuestionTextAreaId').val('');
                getAllQuestions()
            }
        })

    }) 
}

setInterval(checkLatestNotifications, 2500);

function checkLatestNotifications(){

    dataObj = { 'notificationCheck': "check" }
    
    var final_data = {
        'data': JSON.stringify(dataObj),
        csrfmiddlewaretoken: CSRF_TOKEN,
    }

    $.post(CONFIG['domain'] + "/api/Check-latest-notifications", final_data, function (res) {

        if (res.statusCode == 0){ 
            
            notifiCount = res.data['count']

            if(notifiCount != 0){

                $('#notificationBadge').text(notifiCount)

            }
            else{
                $('#notificationBadge').text()
            }

        }

    })
}