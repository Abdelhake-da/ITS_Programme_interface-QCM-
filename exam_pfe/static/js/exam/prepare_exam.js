function get_max_num(checkbox) {
    let max = document.getElementById("max_questions");
    let nb_questions = document.getElementById("nb_questions");
    max_v = parseInt(max.textContent)
    let nb_ques = parseInt(checkbox.getAttribute('nb_ques'))
    if (checkbox.checked) {
        max_v = max_v + nb_ques
    } else {
        max_v = max_v - nb_ques
    }
    if (max.textContent == 0 || nb_questions.value > max_v) {
        if (max_v < 20) {
            nb_questions.value = parseInt(max_v / 2)
        } else {
            nb_questions.value = 10
        }
    }
    nb_questions.max = max_v
    max.textContent = max_v
}