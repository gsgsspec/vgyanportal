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

    // console.log('getScreenWidth :: ', getScreenWidth)

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