
$(document).ready(function () {
    callApi()
})

function callApi(){

    dataObj = {

    }

    var final_data = {
        'data': JSON.stringify(dataObj),
        csrfmiddlewaretoken: CSRF_TOKEN,
    }

    $.post(CONFIG['domain'] + "/api/assessmentslist", final_data, function (res) { 
        
        if ( parseInt(res.statusCode) ===  0 ){
            getAssessmentsList()
        }
    })
}


function getAssessmentsList(){
    $('#assessmentCardsConatainer').append(
        '<div class="col-12 col-md-12 col-lg-12 my-2" > '+
        '<div class="card"> '+
          '<div class="my-course-card"> ' +
            '<div class="col-md-12 col-12 col-lg-12">' +
              '<div class="card-body m-0 p-0"> ' +
                '<div class="p-3 col-12">' +
                 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Tenetur velit nostrum porro possimus, molestias ipsum accusamus reiciendis quasi, placeat neque quod dolore delectus assumenda inventore aliquam hic qui omnis saepe?' +
                '</div>'+
              '</div>'+
            '</div>'+
          '</div>'+
        '</div>'+
      '</div>' )
}