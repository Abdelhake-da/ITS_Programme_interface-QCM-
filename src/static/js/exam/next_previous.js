var questions = document.querySelectorAll(".question-div")
function next(question) {
    if (question + 1 < questions.length) {
        questions[question].classList.add("hidden");
        questions[question + 1].classList.remove("hidden");
    }
   

}
function previous(question) {
    if (question != 0) {
        questions[question].classList.add("hidden");
        questions[question - 1].classList.remove("hidden");

    }

}