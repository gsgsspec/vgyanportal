$(document).ready(function(){

    var receivedData = localStorage.getItem('dataObj');
    var courseData = JSON.parse(receivedData)

    var courseId  =  courseData['courseId']
    var moduleId  =  courseData['moduleId']
    var lessionId =  courseData['lessionId']

    getModuleLesson(courseId,moduleId,lessionId)
    // console.log('++++++++++++++++++++++++++++++++')
    // console.log(courseId,moduleId,lessionId)
    // console.log('++++++++++++++++++++++++++++++++')
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
        var question = $('#basic-default-message').val();

    }) 
}

