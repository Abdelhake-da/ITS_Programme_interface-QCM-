
let time = [];
let timers = []
let is_run = [];
var question_num = 0;
let time_sub = document.querySelectorAll(".time")
var timers_ele = document.querySelectorAll(".timer-class")
var num_q = parseInt(document.getElementById('num_q').textContent)
var controllers = document.querySelectorAll(".control")
for (let i = 0; i < num_q; i++) {
    time.push(0);
    timers.push(0)
    is_run.push(false)
    // clearInterval(timers[i]);
}
function startTimer() {
    is_run[question_num] = true;
    controllers[question_num].innerHTML = `<svg  height="800px" width="800px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
                            viewBox="0 0 512 512" xml:space="preserve" >
                            <path d="M256,0C114.617,0,0,114.615,0,256s114.617,256,256,256s256-114.615,256-256S397.383,0,256,0z M224,320
                                c0,8.836-7.164,16-16,16h-32c-8.836,0-16-7.164-16-16V192c0-8.836,7.164-16,16-16h32c8.836,0,16,7.164,16,16V320z M352,320
                                c0,8.836-7.164,16-16,16h-32c-8.836,0-16-7.164-16-16V192c0-8.836,7.164-16,16-16h32c8.836,0,16,7.164,16,16V320z" fill="#b00000" />
                            </svg>`;
    timers[question_num] = setInterval(() => {
        time[question_num] += 1;
        timers_ele[question_num].innerHTML = formatTime(time[question_num]);
  }, 1);
}
function stopTimer() {
    controllers[question_num].innerHTML = `<svg width="800px" height="800px" viewBox="0 0 15 15" xmlns="http://www.w3.org/2000/svg">
                                <path fill-rule="evenodd" clip-rule="evenodd" d="M0 7.5C0 3.35786 3.35786 0 7.5 0C11.6421 0 15 3.35786 15 7.5C15 11.6421 11.6421 15 7.5 15C3.35786 15 0 11.6421 0 7.5ZM6.24904 5.06754C6.40319 4.97808 6.59332 4.97745 6.74807 5.06588L10.2481 7.06588C10.4039 7.1549 10.5 7.32057 10.5 7.5C10.5 7.67943 10.4039 7.8451 10.2481 7.93412L6.74807 9.93412C6.59332 10.0226 6.40319 10.0219 6.24904 9.93246C6.09488 9.84299 6 9.67824 6 9.5V5.5C6 5.32176 6.09488 5.15701 6.24904 5.06754Z" fill="green" />
                            </svg>`;
    is_run[question_num] = false;
    clearInterval(timers[question_num]);
}

function formatTime(time) {
  let milliseconds = time % 1000;
  let seconds = Math.floor(time / 1000) % 60;
  let minutes = Math.floor(time / (1000 * 60));

  return `${minutes}:${seconds.toString().padStart(2, "0")}.${milliseconds}`;
}
function toggle_str_pause() {
    
    element = controllers[question_num]
    if (is_run[question_num]) {
        stopTimer()
        document.querySelector('input[type = "submit"]').disabled = true;
        
    } else {
        startTimer();
        document.querySelector('input[type = "submit"]').disabled = false;
        
    }
    
}
document.getElementById("submit").onclick = () => {
    for (var i = 0; i < time.length; i++) {
        document.getElementsByName("time[]")[i].value = time[i];
    }
};
var questions = document.querySelectorAll(".question-div")
if (controllers.length > 0) {
    startTimer()
}
function next(question) {
    questions[question].classList.add("hidden");
    questions[question + 1].classList.remove("hidden");
    stopTimer()
    question_num += 1;
    startTimer()
    
}
function previous(question) {
    if(question != 0){
        questions[question].classList.add("hidden");
        questions[question - 1].classList.remove("hidden");
        stopTimer()
        question_num -= 1;
        startTimer()

    }
    
}