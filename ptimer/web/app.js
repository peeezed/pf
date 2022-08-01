// function compute() {
//   var textbox = document.getElementById("input");
//   text = textbox.value;
//   eel.sort(text);
// }

// eel.expose(showAnswers)
// function showAnswers(answer) {
//   var output = document.getElementById("result");
//   output.innerHTML = "Result: " + answer;
// }

// const assBtn = document.querySelector(".fuck");

// assBtn.addEventListener("click", () => {
//   compute();
// })

const tempoDisplay = document.querySelector(".tempo");
const lastTempoText = document.querySelector(".tempo-text");
const countdownDisplay = document.querySelector(".timer")
const exerciseName = document.querySelector(".exercise-name")

const decreaseTempoBtn = document.querySelector(".decrease");
const increaseTempoBtn = document.querySelector(".increase");
const startStopBtn = document.querySelector(".start-stop");
const countdownBtn = document.querySelector(".start")
const resetCountdownBtn = document.querySelector(".reset")
const setBtn = document.querySelector(".set")
const chooseExerciseBtn = document.querySelector(".choose-exercise")
const addExerciseButton = document.querySelector(".add")
const removeExerciseBtn = document.querySelector(".remove");
const updateExerciseBpmBtn = document.querySelector(".update-bpm-exercise");
const updateExerciseNameBtn = document.querySelector(".update-name-exercise");
const exerciseBtns = document.querySelector(".exercise-btns")

const tempoSlider = document.querySelector(".slider");

const minuteInput = document.querySelector(".minutes")
const secondInput = document.querySelector(".seconds")

const dropdownMenu = document.querySelector(".dropdown")
const imageFrame  = document.querySelector(".img-frame")


let minutes = parseInt(minuteInput.value) * 60 || 0;
let seconds = parseInt(secondInput.value) || 0;
let originalTimer = (minutes + seconds);
let timer = originalTimer;
let bpm = tempoSlider.value;
let paused = true;
let exercisesArray = []



var metronome = new Metronome();

const ding = new Audio("/sound/dingshort.mp3");


tempoDisplay.textContent = bpm;
lastTempoText.textContent = "" // Read from save
eel.relay_exercises(add_dropdown = true);


function refreshExercises(add_dropdown = false) {
  exercisesArray = [];
  if(add_dropdown) {
    eel.relay_exercises(add_dropdown = true);
  } else {
    exercisesArray = [];
    eel.relay_exercises();
  }
}

addExerciseButton.addEventListener("click", () => {
  eel.save_exercises(`Exercise - ${exercisesArray.length + 1}`, 130);
  refreshExercises(add_dropdown = true)
})

removeExerciseBtn.addEventListener("click", () => {
  const [url, exBpm, exId, exName] = getExercise();
  const choice = confirm(`Do you want to delete: ${exName}?`)
  if (choice == true) {
    eel.delete_exercise(exId);
    alert("Entry Deleted");
    refreshExercises(add_dropdown = true)
  } else {
    return
  }
})

updateExerciseBpmBtn.addEventListener("click", () => {
  const [url, exBpm, exId, exName] = getExercise();
  eel.update_exercise(exId, exName, bpm);
  alert("Entry Updated");
  refreshExercises()
})

updateExerciseNameBtn.addEventListener("click",()=> {
  const [url, exBpm, exId, exName] = getExercise();
  const newName = exerciseName.value;
  eel.update_exercise(exId, newName, exBpm);
  alert("Entry Updated");
  refreshExercises()
  dropdownMenu.options[dropdownMenu.selectedIndex].text = newName;
})


dropdownMenu.addEventListener("change", () => {
  const [url, exBpm, exId, exName] = getExercise();
  lastTempoText.textContent = `Last Practice was: ${exBpm || "unknown"} bpm`;
  exerciseName.classList.remove("hidden")
  exerciseName.value = exName;

  bpm = exBpm || 120;
  updateMetronome();

  exerciseBtns.classList.remove("hidden")
  imageFrame.classList.remove("hidden")
  imageFrame.innerHTML = `
  <img class="tab" src="${url}" alt="${exName}">
  `;
});

setBtn.addEventListener("click", () => {
  minutes = parseInt(minuteInput.value) * 60 || 0;
  seconds = parseInt(secondInput.value) || 0;
  originalTimer = minutes + seconds;
  timer = originalTimer;
  paused = true;
  countdownBtn.textContent = "Start Countdown";
});

tempoSlider.addEventListener("input", () => {
  bpm = tempoSlider.value;
  updateMetronome();
});

increaseTempoBtn.addEventListener("click", () => {
  if (bpm >= 230) {return}
  bpm++;
  updateMetronome();
});

decreaseTempoBtn.addEventListener("click", () => {
  if (bpm <= 40) {return}
  bpm--;
  updateMetronome();
});

startStopBtn.addEventListener("click", () => {
  metronome.tempo = bpm;
  metronome.startStop();

  if (metronome.isRunning) {
    startStopBtn.textContent = "STOP"
  } else {
    startStopBtn.textContent = "START"
  }
});

countdownBtn.addEventListener("click",()=> {
  if (timer == 0) { return }
  if (paused) {
    paused = false;
    eel.countdown(timer)
    countdownBtn.textContent = "Pause Countdown"
  } else {
    paused = true;
    countdownBtn.textContent = "Start Countdown"
  } 
});

resetCountdownBtn.addEventListener("click", () => {
  paused = true;
  timer = originalTimer;
  eel.countdown(timer);
  countdownBtn.textContent = "Start Countdown";
});

eel.expose(showCountdown)
function showCountdown(mins,secs,remaining) {
  if (remaining > 0) {
    timer = remaining
    minuteInput.value = mins;
    secondInput.value = secs;
  } else {
    timer = remaining
    minuteInput.value = mins;
    secondInput.value = secs;
    ding.play();
  }
}

function updateMetronome() {
  tempoDisplay.textContent = bpm;
  tempoSlider.value = bpm;
  metronome.tempo = bpm;
}

eel.expose(isPaused)
function isPaused() {
  return paused
}

eel.expose(addExercises) 
function addExercises(exercises){
  let i = 0;
  for(const exercise of exercises) {
    const exerciseObj = {
      exName: exercise[0],
      bpm : exercise[1],
      url : exercise[2],
      id : exercise[3],
      index : i,
    };
    exercisesArray.push(exerciseObj)
    i++;
  }
}

eel.expose(addDropdown)
function addDropdown() {
  if (exercisesArray.length == 0) {
    dropdownMenu.innerHTML =
    '<option value="" selected disabled hidden>Use Add Button</option>';
  }
  else {
    dropdownMenu.innerHTML =
    '<option value="" selected disabled hidden>Choose Exercise</option>';
  }
  for (const obj of exercisesArray) {
    dropdownMenu.innerHTML += `
    <option value="${obj["index"]}">${obj["exName"]}</option>
    `;
  }
}

function getExercise() {
  const exIndex = dropdownMenu.value;
  // console.log(exValues);
  exercise = exercisesArray[exIndex];

  url = exercise["url"];
  exBpm = exercise["bpm"];
  exId = exercise["id"];
  exName = exercise["exName"];

  return [url, exBpm, exId, exName];
}
