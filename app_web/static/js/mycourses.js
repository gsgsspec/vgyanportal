var showMoreChecked = []

// Show card depends on Screen Size
window.addEventListener("resize", handleResize);
function handleResize() {
    var getScreenWidth = screen.width
    showCoursesCards(getScreenWidth)
}

document.addEventListener("DOMContentLoaded", function () {
    var getScreenWidth = screen.width

    showCoursesCards(getScreenWidth)

    // notifications
    getNotifications()
});

function showCoursesCards(getScreenWidth) {

    if (getScreenWidth >= 992) {
        largeScreenView()
    }
    else {
        smallScreenView()
    }

}

var getChildren = document.getElementById('CourseCardContainer').children;
var cardsCount = getChildren.length;

function largeScreenView() {

    if (cardsCount <= 4){
        document.getElementById('showMoreId').classList.add('d-none')
    }

    for (var child = 0; child < cardsCounts; child++) {
        var childId = getChildren[child].id;

        if (child < 4) {
            document.getElementById(childId).classList.remove('d-none')
        }

    }
}

function smallScreenView() {

    if (cardsCount <= 2){
        document.getElementById('showMoreId').classList.add('d-none')
    }

    for (var child = 0; child < cardsCounts; child++) {

        var childId = getChildren[child].id;
        document.getElementById(childId).classList.add('d-none')

        if (child < 2) {
            document.getElementById(childId).classList.remove('d-none')
        }
    }

}
// Show card depends on Screen Size End


// Show More Button start's 

var getChildrens = document.getElementById('CourseCardContainer').children;
var cardsCounts = getChildrens.length;

function showMore(event) {
    var getScreenWidth = screen.width

    event.preventDefault()

    if (showMoreChecked[0] === undefined) {

        for (var Card = 0; Card < cardsCounts; Card++) {
            document.getElementById(getChildrens[Card].id).classList.remove('d-none');
        }

        document.getElementById('showMoreId').textContent = 'Show Less';
        showMoreChecked.push('SHOW')

    }
    else {

        var getScreenWidth = screen.width

        if (getScreenWidth >= 992) {

            for (var Card = 0; Card < cardsCounts; Card++) {

                document.getElementById(getChildrens[Card].id).classList.add('d-none');

                if (Card < 4) {
                    document.getElementById(getChildrens[Card].id).classList.remove('d-none');
                }

            }

            document.getElementById('showMoreId').textContent = 'Show More';
            showMoreChecked = []
        }
        else {

            for (var Card = 0; Card < cardsCounts; Card++) {

                document.getElementById(getChildrens[Card].id).classList.add('d-none');

                if (Card < 2) {
                    document.getElementById(getChildrens[Card].id).classList.remove('d-none');
                }

            }

            document.getElementById('showMoreId').textContent = 'Show More';
            showMoreChecked = []
        }

    }

}

// Show More Button End's

// Refersh Notifications

// setInterval(getNotifications, 2000);

// Notifications

var notificationCounter = 5




function getNotifications(){

    dataObj = {
        'notifications': 'Y',
        'notificationFor' : "HomePage",
        'notificationCount': notificationCounter,
    }

    var final_data = {
        'data': JSON.stringify(dataObj),
        csrfmiddlewaretoken: CSRF_TOKEN,
    }
    
    $.post(CONFIG['domain'] + "/api/all-notifications", final_data, function (res) {
        if(res.statusCode == 0){
            var allNotificationList = res.data
            var showMoreNotifications = res.data2
            console.log('showMoreNotifications :: ',showMoreNotifications)
            if (allNotificationList != "EMPTY"){

                showNotifications(allNotificationList,showMoreNotifications)

            }
            else{

                noNotifications()

            }
        
        }

    })

}

// Show Notifications Start

function showNotifications(allNotificationList,itearations,showMoreNotifications){

    var numberofNotifications = allNotificationList

    var looper = 5
    console.log('showMoreNotifications FUN:: ',showMoreNotifications)
    if (showMoreNotifications ===  "Y"){

        $('#showMoreContainer').css('display','flex')

    }
    else{

        $('#showMoreContainer').css('display','none')
        
        if(numberofNotifications.length == 0){
            $('#showMoreContainer').css('display','none')
            $('#noNotificationsContainer').css('display','flex')
        }
        else{
            looper = numberofNotifications.length
        }

    }

    var noNotificationId = $("#notificationsContainer")
    noNotificationId.html('')

    for(var notifi = 0; notifi < numberofNotifications.length; notifi ++){

        var identity         = numberofNotifications[notifi]['identity']
        var courseTitle      = numberofNotifications[notifi]['coursetitle']
        var courseModule     = numberofNotifications[notifi]['coursemoduletitle']
        var notificationTime = numberofNotifications[notifi]['notificationDate'] // notification time
        var notificationFor  = numberofNotifications[notifi]['notificationEventType'] // Question Or Assessment
        var notificationMessage = numberofNotifications[notifi]['notificationMessage'] 
        var notificationStatus  = numberofNotifications[notifi]['notificationStatus']  // cleared or Deleated
        var notificationDataType  = numberofNotifications[notifi]['notificationDataType'] // Warning or Danger or Information

        if(notificationStatus != "C" && notificationStatus != 'D'){

            var notificationBarColor = 'success'

            if(notificationDataType == 'I'){
                notificationBarColor = 'primary'
            }

            if(notificationDataType == 'S'){
                notificationBarColor = 'success'
            }

            if(notificationDataType == 'W'){
                notificationBarColor = 'warning'
            }

            if(notificationDataType == 'D'){
                notificationBarColor = 'danger'
            }

            var iconChange = ''
            var fontSize = ''
            var Padding = ''

            if(notificationFor == 'Q'){
                iconChange = 'far fa-question-circle p-clr'
                fontSize = '25px'
                Padding = '7px'
            }

            if(notificationFor == 'A'){
                iconChange = 'fas fa-clipboard-check p-clr'
                fontSize = '20px'
                Padding = '10px 12px'
            }


            noNotificationId.append(
                '<div id="alertContainer'+identity+'" class="alert alert-'+notificationBarColor+' alert-dismissible" role="alert" style="padding: 0.7375rem 0.7375rem">' +
                   ' <div style="display: flex; align-items: center;">' +
                        '<span id="iconCardContainer" class="card" style="width: max-content; margin-right:10px; padding:'+Padding+'; ">' +
                          '<i id="notificationIcon" class="'+iconChange+'" style="font-size:'+fontSize+';"></i>' +
                        '</span>' +
                        '<span style="display: flex; flex-direction: column;">' +
                         ' <span class="text_color_custom">Your Question in '+ courseTitle +' is Posted</span>' +
                         ' <div class="alert p-0 m-0" style="float:left; background-color: transparent !important;" >' +
                            '<div style="display:flex; font-size: small;">' +
                              '<span>' +
                                '<span class="alert-secondary text_color_custom" style="background-color: transparent !important;">' +
                                 ''+notificationTime+''+
                                '</span>' +
                              '</span>' +
                            '</div>' +
                          '</div>' +
                        '</span>'+
                    '</div>' +
                    '<i onclick="removeNotification(this.id)" id="removenotificationbtn_'+identity+'" data_notification_id="'+identity+'" class="btn-close text_color_custom fas fa-times" data-bs-dismiss="alert" aria-label="Close" style="top: 6px; width: 5%; font-size: 17px; cursor: pointer; background: url(""); background-image:url(""); "></i>' +
                  '</div>'
            )

        }

    }
    
}

// Show Notifications End

// No Notifications Start

function noNotifications(){
    
    var noNotificationId = $("#notificationsContainer")
    noNotificationId.html('')
    noNotificationId.css('display','flex')
    noNotificationId.append(
        "<div class='container' style='display: flex; justify-content: center;'>" +
        "<div>" +
          "<h5 class='card-header' style='display: flex; justify-content: center; align-items: center;' >" +
            "<i class='tf-icons bx bx-bell p-clr' style='font-size: 25px;'></i> &nbsp;" +
            "<span style='color: rgba(128, 128, 128, 0.807);'>" +
            "  No Notifications Here" +
            "</span>" +
          "</h5>" +
        "</div>" +
      "</div>"
    );
    
}

// No Notifications End

// Remove Notification

function removeNotification(data){

    var notifiID = data.split("_")

    var removeNotificId = notifiID[1]

    dataObj = {
        'notificationsId': removeNotificId,
        'status'         : 'C'
    }

    var final_data = {
        'data': JSON.stringify(dataObj),
        csrfmiddlewaretoken: CSRF_TOKEN,
    }
    
    $.post(CONFIG['domain'] + "/api/remove-notification", final_data, function (res) {

        if (res.statusCode == 0){
            getNotifications()
        }

    })

}

$('#showMoreContainer').click(function (e) { 
    e.preventDefault();

    getNotifications()

});