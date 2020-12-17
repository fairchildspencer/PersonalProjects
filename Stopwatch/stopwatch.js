window.onload = function () {

    let seconds = 00; 
    let tens = 00; 
    let minutes = 00;
    let appendMinutes = document.getElementById("minutes");
    let appendTens = document.getElementById("tens")
    let appendSeconds = document.getElementById("seconds")
    let start = document.getElementById('button-start');
    let stop = document.getElementById('button-stop');
    let reset = document.getElementById('button-reset');
    let Interval;

    start.onclick = function () {
        clearInterval(Interval);
        Interval = setInterval(startTimer, 10);
    }

    stop.onclick = function () {
        clearInterval(Interval);
    }

    reset.onclick = function () {
        clearInterval(Interval);
        minutes = "0" + 0;
        tens = "0" + 0;
        seconds = "0" + 0;
        appendSeconds.innerHTML = seconds;
        appendTens.innerHTML = tens;
        appendMinutes.innerHTML = minutes;
    }

    function startTimer() {
        tens++; 
    
        if(tens < 9){
            appendTens.innerHTML = "0" + tens;
        }
    
        if (tens > 9){
            appendTens.innerHTML = tens;
        
        } 
    
        if (tens > 99) {
            seconds++;
            appendSeconds.innerHTML = "0" + seconds;
            tens = 0;
            appendTens.innerHTML = "0" + 0;
        }
    
        if (seconds > 9){
        appendSeconds.innerHTML = seconds;
        }

        if (seconds > 59) {
            minutes++;
            appendMinutes.innerHTML = "0" + minutes;
            seconds = 0;
            appendSeconds.innerHTML = "0" + 0;
        }

        if (minutes > 9) {
            appendMinutes.innerHTML = minutes;
        }
  
  }

}