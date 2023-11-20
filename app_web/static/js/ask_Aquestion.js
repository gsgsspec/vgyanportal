$(document).ready(function(){
    getModuleLesson()
    // askQuestionInputField()
})


// function askQuestionInputField(){
//     $('#askaQuestionCardContainer').append(

//         ' <div class="col-12 col-md-12 col-lg-6">' +
//                         '<div class="card mb-3">'  +
//                           '<div class="my-course-card">' +
//                             '<div class="m-3 col-md-4 my-courses-images"></div>' +
//                             '<div class="col-md-8 my-course-card-body">' +
//                               '<div class="card-body m-0 p-0">' +
//                                 '<h5 class="card-title"></h5>'  +
//                                 '<p> </p>' +
                                
//                               '</div>' +
//                             '</div>'   +
//                          '</div>'      +
//                         '</div>'       +
//                       '</div>'         
// )}

var receivedData = localStorage.getItem('dataObj');
courseData = JSON.parse(receivedData)

courseId  =  courseData['courseId']
moduleId  =  courseData['moduleId']
lessionId =  courseData['lessionId']

function getModuleLesson(){
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
        console.log('res',res.data.Modules);
        console.log('res',);

        var getModulesDataList = res.data.Modules;
        var getLessonsDataList = res.data.lesson;
    
        if (res.statusCode == 0){

            for (var modul = 0 ; modul < getModulesDataList.length; modul ++){

                var moduleName = getModulesDataList[modul]['moduleName']
                var moduleId = getModulesDataList[modul]['moduleId']

                if (getModulesDataList[modul]['selected'] === "YES"){

                    $('#moduleId').append(
                        '<option selected value="'+ moduleId +'" id="'+ moduleName +'_'+ moduleId  +'"> ' + moduleName + '   </option>'
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
                        '<option selected value="'+ lessonId +'" id="'+ lessonName+ '_' + lessonId +'" > ' + lessonName + ' </option>'
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
        var question = $('#basic-default-message').val();

    }) 
}

