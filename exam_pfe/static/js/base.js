var form = document.getElementById('add-form')
var form_container = document.getElementById('form_container')
var choices = document.getElementById('choices')
var text_choice = document.getElementById('text-choice')
var is_correct = document.getElementById('correct')

function showAddForm() {
    form.classList.remove('hidden')
    form_container.classList.add('disabled')
}
function hidden_form() {
    form.classList.add('hidden')
    form_container.classList.remove('disabled')

}
function addChoice() {
    const li = document.createElement('li')
    li.classList.add('choice-list')
    // const sanitizedText = text_choice.value.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    li.innerHTML = `
    <p>${text_choice.value} , ${is_correct.checked}</p>
    <input type="hidden" name="choices[]" value='${text_choice.value.replace(/"/g, '&quot;').replace(/'/g, '&#39;') }'/>
    <input type="hidden" name="is_correct[]"  value='${Number(is_correct.checked)}'/>
    <button class="btn btn-danger" onclick="this.parentElement.remove()">Delete</button>
    `
    choices.appendChild(li)
    text_choice.value = ''
    is_correct.checked = false
    
}
function edit_question(element) {
    choices.innerHTML = ''
    element = element.parentElement
    course_name = element.querySelector('.course').innerText.trim()
    course_id = element.querySelector('.course').getAttribute('course_id')
    question_name = element.querySelector('.question').innerText.trim()
    question_id = element.querySelector('.question').getAttribute('question_id')
    correctAnswer = element.querySelectorAll('.correctAnswer ul li')
    choices_list = element.querySelectorAll('.choices ul li')
    correct_list = []
    for (let i = 0; i < correctAnswer.length; i++){
        correct_list.push(correctAnswer[i].innerText.trim())
    }
    console.log(correct_list)
    for (let i = 0; i < choices_list.length; i++){
        const li = document.createElement('li')
        li.classList.add('choice-list')
        correct = correct_list.includes((i+1).toString());
        if (correct) {
            li.innerHTML = `
            <p>${choices_list[i].innerText.trim()} , ${correct}</p>
            <input type="hidden" name="choices[]" value='${choices_list[i].innerText.trim().replace(/"/g, '&quot;').replace(/'/g, '&#39;')}'/>
            <input type="hidden" name="is_correct[]"  value='${Number(correct)}'/>
            <button class="btn btn-danger" onclick="this.parentElement.remove()">Delete</button>
        `
        } else {
            li.innerHTML = `
                <p>${choices_list[i].innerText.trim()} , ${correct}</p>
                <input type="hidden" name="choices[]" value='${choices_list[i].innerText.trim().replace(/"/g, '&quot;').replace(/'/g, '&#39;')}'/>
                <input type="hidden" name="is_correct[]"  value='${Number(correct)}'/>
                <button class="btn btn-danger" onclick="this.parentElement.remove()">Delete</button>
            `
        }
        choices.appendChild(li)
        
    }
    document.getElementById('edit-hidden').value = question_id
    document.getElementById('id_course').value = course_id
    document.getElementById('id_question_text').value = question_name
    showAddForm()
}