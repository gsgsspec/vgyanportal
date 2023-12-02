var receivedData = localStorage.getItem('dataObj');
var courseData = JSON.parse(receivedData)

var courseId  =  courseData['courseId']

var getQuestionData = {
    'courseId' : courseId,
    'userId'   : '' //user getting in backend request.user
    }

var getModulesList = {
    'courseId' : courseId,
    'moduleId' : 0,
}

$(document).ready(function(){
    
    getModuleLesson(getModulesList)

    getQuestionsList(getQuestionData)
})

$('#moduleId').change(function(){

    var getModulesList = {
        'courseId' : courseId,
        'moduleId' : $('#moduleId').val(),
    }

    getModuleLesson(getModulesList)
})


// function getModuleLesson(getModulesList){

//     var dataobj = getModulesList

//     var final_data = {
//         'data': JSON.stringify(dataobj),
//         csrfmiddlewaretoken: CSRF_TOKEN,
//     }

//     $.post(CONFIG['domain'] + "/api/get-module-lessons", final_data, function (res) {
        
//         var getModulesDataList = res.data.Modules;
//         var getLessonsDataList = res.data.lesson;

//         if (res.statusCode == 0){

//             $('#moduleId').html('')
//             $('#lessonId').html('')

//             if (getModulesDataList.length == 0){
//                 $('#moduleId').prop('disabled', true);
//                 $('#moduleId').append(
//                     '<option  value="" id=""> ' + " No Modules " + ' </option>'
//                 )
//             }
//             else{
//                 $('#moduleId').prop('disabled', false);
//             }

//             if (getLessonsDataList.length == 0){
//                 $('#lessonId').prop('disabled', true);
//                 $('#lessonId').append(
//                     '<option  value="" id=""> ' + " No Lessons " + ' </option>'
//                 )
//             }
//             else{
//                 $('#lessonId').prop('disabled', false);
//             }
            

//             for (var modul = 0 ; modul < getModulesDataList.length; modul ++){

//                 var moduleName = getModulesDataList[modul]['moduleName']
//                 var moduleId = getModulesDataList[modul]['moduleId']

//                 if (getModulesDataList[modul]['selected'] === "YES"){

//                     $('#moduleId').append(
//                         '<option  value="'+ moduleId +'" id="'+ moduleName +'_'+ moduleId  +' " selected> ' + moduleName + '   </option>'
//                     )

//                 }
//                 else{
//                     $('#moduleId').append(
//                         '<option value="'+ moduleId +'" id="'+ moduleName +'_'+ moduleId  +'"> ' + moduleName + '   </option>'
//                     )
//                 }

//             }

//             for (var lesson = 0 ; lesson < getLessonsDataList.length; lesson ++){
                
//                 var lessonName = getLessonsDataList[lesson]['title'];
//                 var lessonId = getLessonsDataList[lesson]['lessonid']; 

//                 if (getLessonsDataList[lesson]['defaultLesson'] === "YES"){

//                     $('#lessonId').append(
//                         '<option value="'+ lessonId +'" id="'+ lessonName+ '_' + lessonId + '"  selected > ' + lessonName + ' </option>'
//                     )

//                 }
//                 else{
//                     $('#lessonId').append(
//                         '<option value=" '+ lessonId +' " id=" '+ lessonName+ '_' + lessonId +' "> ' + lessonName + ' </option>'
//                     )
//                 }

//             }

//         }
//     })

// }


function getModuleLesson(getModulesList){

    var dataobj = getModulesList

    var final_data = {
        'data': JSON.stringify(dataobj),
        csrfmiddlewaretoken: CSRF_TOKEN,
    }

    $.post(CONFIG['domain'] + "/api/get-module-lessons", final_data, function (res) {
        
        console.log('res :: ',res.data.courseName)
        console.log('res :: ',res.data.courseModuleName)
        console.log('res :: ',res.data.courseLessonName)

        var getCourseName  = res.data.courseName
        var getModuleName  = res.data.courseModuleName;
        var getLessonsName = res.data.courseLessonName;

        if (res.statusCode == 0){

            $('#courseId').text(getCourseName)

            $('#moduleContainer').html('')
            $('#moduleContainer').text(getModuleName)

            $('#lessonContainer').html('')
            $('#lessonContainer').text(getLessonsName)

        }
    })

}


function askQuestion(){

    $('#askQuestionForm').unbind('submit').bind('submit',function(event){
        event.preventDefault();

        // var courseId = $('#courseId').attr('data-course-id');
        var moduleId = $('#moduleId').val();
        var lessonId = $('#lessonId').val();
        var question = $('#AskQuestionTextAreaId').val();

        dataObj = {
            'courseId':  courseId,
            'moduleId':  moduleId,
            'lessonId':  lessonId,
            'question':  question,
        }
        // console.log('dataObj :: ',dataObj)

        var final_data = {
            'data': JSON.stringify(dataObj),
            csrfmiddlewaretoken: CSRF_TOKEN,
        }

        $.post(CONFIG['domain'] + "/api/save-question", final_data, function (res) {
            // console.log('res',res);
        
            if (res.statusCode == 0){
                $('#AskQuestionTextAreaId').val('');
                showSuccessMessage('Question add')
                getQuestionsList(getQuestionData)
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
    
            var answeredQuestion = res.data.questionList;
            var overAllQuestions = res.data.overAllQuestions;
            // console.log('res.data :: ',res.data.sendUserId)
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

                        $('#vertical-example').append(
                            '<div class="accordion-item card m-2">' +
                            '<h2 class="accordion-header" id="headingOne' + questionId + '">' +
                            '<button type="button" class="accordion-button collapsed" data-bs-toggle="collapse" data-bs-target="#accordionOne' + questionId + '" aria-expanded="false" aria-controls="accordionOne' + questionId + '">' +
                            question + ' </button>' +
                            '</h2>' +
                            '<div id="accordionOne' + questionId + '" class="accordion-collapse collapse" data-bs-parent="#accordionExample">' +
                            '<div class="accordion-body"> ' + questionAnswer + ' </div>' +
                            '</div>' +
                            '</div>'
                        );

                    }

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
        });
    }