let timer;
let time = 0;
function startTimer() {
  timer = setInterval(() => {
    time += 1;
    document.getElementById("timer").innerHTML = formatTime(time);
  }, 1);
}

function formatTime(time) {
  let milliseconds = time % 1000;
  let seconds = Math.floor(time / 1000) % 60;
  let minutes = Math.floor(time / (1000 * 60));

  return `${minutes}:${seconds.toString().padStart(2, "0")}.${milliseconds}`;
}
document.getElementById("stop").onclick = () => {
  clearInterval(timer);
  document.querySelector('input[type = "submit"]').disabled = true;
  document.querySelector('input[type = "number"]').disabled = true;
  document.getElementById("play").autofocus = true;
};

document.getElementById("play").onclick = () => {
  startTimer();
  document.querySelector('input[type = "submit"]').disabled = false;
  document.querySelector('input[type = "number"]').disabled = false;
  document.querySelector('input[type = "number"]').autofocus = true;
};

document.getElementById("submit").onclick = () => {
  document.getElementById("time").value = time;
};

startTimer();
