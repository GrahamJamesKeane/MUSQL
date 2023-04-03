var timerDisplay = document.getElementById('timer');
var submitBtn = document.getElementById('assignment-form');

/**
 * Starts a timer that counts down from the specified duration and displays the time remaining in the specified element.
 * When the timer reaches 0, it clears the interval and submits the form. 
 * @param {number} duration - The duration of the timer in seconds. 
 * @param {HTMLElement} timerDisplay - The element to display the time remaining in. 
 * @param {HTMLElement} submitBtn - The submit button to click when the timer runs out.
 */
var timer = setInterval(function () {
    duration--;
    var minutes = Math.floor(duration / 60);
    var seconds = duration % 60;
    timerDisplay.innerHTML = 'Time Remaining: ' + minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
    if (duration == 0) {
        clearInterval(timer);
        submitBtn.click(); // automatically submit when time runs out
    }
}, 1000);