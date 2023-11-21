$(document).ready(function(){

    var receivedData = localStorage.getItem('dataObj');
    var courseData = JSON.parse(receivedData)

    var courseId  =  courseData['courseId']
    var moduleId  =  courseData['moduleId']
    var lessionId =  courseData['lessionId']

    getModuleLesson(courseId,moduleId,lessionId)

    var getQuestionData = {
        'courseId' : 1,
        'userId'   : 1
        }

    getQuestionsList(getQuestionData)
})

$('#moduleId').change(function(){

    console.log( $('#moduleId').val() )

    var courseId  =  1 
    var moduleId  =  $('#moduleId').val()
    var lessionId =  0

    getModuleLesson(courseId,moduleId,lessionId)
})


function getModuleLesson(courseId,moduleId,lessionId){

    var dataobj = {
        'courseId'  : courseId,
        'moduleId'  : moduleId,
        'lessionId' : lessionId
    }

    var final_data = {
        'data': JSON.stringify(dataobj),
        csrfmiddlewaretoken: CSRF_TOKEN,
    }

    $.post(CONFIG['domain'] + "/api/get-module-lessons", final_data, function (res) {

        var getModulesDataList = res.data.Modules;
        var getLessonsDataList = res.data.lesson;
    
        if (res.statusCode == 0){

            $('#moduleId').html('')
            $('#lessonId').html('')

            for (var modul = 0 ; modul < getModulesDataList.length; modul ++){

                var moduleName = getModulesDataList[modul]['moduleName']
                var moduleId = getModulesDataList[modul]['moduleId']

                if (getModulesDataList[modul]['selected'] === "YES"){

                    $('#moduleId').append(
                        '<option  value="'+ moduleId +'" id="'+ moduleName +'_'+ moduleId  +' " selected> ' + moduleName + '   </option>'
                    )

                }
                else{
                    $('#moduleId').append(
                        '<option value="'+ moduleId +'" id="'+ moduleName +'_'+ moduleId  +'"> ' + moduleName + '   </option>'
                    )
                }

            }

            for (var lesson = 0 ; lesson < getLessonsDataList.length; lesson ++){
                
                var lessonName = getLessonsDataList[lesson]['title'];
                var lessonId = getLessonsDataList[lesson]['lessonid']; 

                if (getLessonsDataList[lesson]['defaultLesson'] === "YES"){

                    $('#lessonId').append(
                        '<option value="'+ lessonId +'" id="'+ lessonName+ '_' + lessonId + '"  selected > ' + lessonName + ' </option>'
                    )

                }
                else{
                    $('#lessonId').append(
                        '<option value=" '+ lessonId +' " id=" '+ lessonName+ '_' + lessonId +' "> ' + lessonName + ' </option>'
                    )
                }

            }

        }
    })

}


function askQuestion(){

    $('#askQuestionForm').unbind('submit').bind('submit',function(event){
        event.preventDefault();

        var courseId = $('#courseId').attr('data-course-id');
        var moduleId = $('#moduleId').val();
        var lessonId = $('#lessonId').val();
        var question = $('#AskQuestionTextAreaId').val();

        dataObj = {
            'courseId':  courseId,
            'moduleId':  moduleId,
            'lessonId':  lessonId,
            'question':  question
        }

        var final_data = {
            'data': JSON.stringify(dataObj),
            csrfmiddlewaretoken: CSRF_TOKEN,
        }

        $.post(CONFIG['domain'] + "/api/save-question", final_data, function (res) {
            console.log('res',res);
        
            if (res.statusCode == 0){
                $('#AskQuestionTextAreaId').val('');
                showSuccessMessage('Question add')
            }
        })

    }) 
}

function getQuestionsList(getQuestionData) {
    dataObj = {
        'getQuestionData': getQuestionData
    }

    var final_data = {
        'data': JSON.stringify(dataObj),
        csrfmiddlewaretoken: CSRF_TOKEN,
    }

    $.post(CONFIG['domain'] + "/api/get-questions", final_data, function (res) {

        console.log('res', res);

        var answeredQuestion = res.data.questionList;
        var unansweredQuestion = res.data.unansweredQuestion;

        if (res.statusCode == 0) {

            for (var ans = 0; ans < answeredQuestion.length; ans++) {

                var question = answeredQuestion[ans]['ques'];
                var questionId = answeredQuestion[ans]['id'];
                var questionAnswer = answeredQuestion[ans]['ans'];

                console.log('question ::: ', question);

                $('#questionsId').append(
                    '<div class="card accordion-item">' +
                    '<h2 class="accordion-header" id="headingOne' + questionId + '">' +
                    '<button type="button" class="accordion-button" data-bs-toggle="collapse" data-bs-target="#accordionOne' + questionId + '" aria-expanded="false" aria-controls="accordionOne' + questionId + '">' +
                    question + ' </button>' +
                    '</h2>' +
                    '<div id="accordionOne' + questionId + '" class="accordion-collapse collapse" data-bs-parent="#accordionExample">' +
                    '<div class="accordion-body"> ' + questionAnswer + ' </div>' +
                    '</div>' +
                    '</div>'
                );
            }
        }
    });
}