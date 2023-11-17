var showMoreChecked = []
var getScreenWidth = screen.width

// Show card depends on Screen Size
window.addEventListener("resize", handleResize);
function handleResize() {
    showCoursesCards()
}

document.addEventListener("DOMContentLoaded", function () {
    showCoursesCards()
});

function showCoursesCards(){
    
    if (getScreenWidth >= 992){
        largeScreenView()
    }
    else{
        smallScreenView()
    }

}

var getChildren = document.getElementById('CourseCardContainer').children;
var cardsCount = getChildren.length;

function largeScreenView() {

    for (var child = 0; child < 4; child++) {
        
        var childId = getChildren[child].id;

        if (cardsCount) {
            document.getElementById(childId).classList.remove('d-none')
        }
    }
}

function smallScreenView(){

    for (var child = 0; child < 6; child++) {
        var childId = getChildren[child].id;
        document.getElementById(childId).classList.add('d-none')
    }

    for (var child = 0; child < 2; child++) {
        
        var childId = getChildren[child].id;
        document.getElementById(childId).classList.add('d-none')

        if (cardsCount) {
            document.getElementById(childId).classList.remove('d-none')
        }
    }

}
// Show card depends on Screen Size End


// Show More Button start's 

var getChildrens = document.getElementById('CourseCardContainer').children;
var cardsCounts = getChildrens.length;

function showMore(event){
    event.preventDefault()
    
    if (showMoreChecked[0] === undefined) {

        for (var Card = 0 ; Card < cardsCounts ; Card ++ ){
            document.getElementById(getChildrens[Card].id).classList.remove('d-none');
        }
        document.getElementById('showMoreId').textContent = 'Show Less'; 
        showMoreChecked.push('SHOW')

    }
    else{

        if (getScreenWidth >= 992){
            for (var Card = 0 ; Card < 2 ; Card ++ ){
                document.getElementById(getChildrens[Card].id).classList.add('d-none');  
            }
    
            document.getElementById('showMoreId').textContent = 'Show More';
            showMoreChecked = []
        }
        else{
            
            for (var Card = 0 ; Card < 4 ; Card ++ ){
                document.getElementById(getChildrens[Card].id).classList.add('d-none');   
            }
    
            document.getElementById('showMoreId').textContent = 'Show More';
            showMoreChecked = []
        }


    }

}


// Show More Button End's