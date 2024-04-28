// csrftoken
// https://docs.djangoproject.com/en/5.0/howto/csrf/#using-csrf-protection-with-ajax
// https://docs.djangoproject.com/en/5.0/howto/csrf/#setting-the-token-on-the-ajax-request
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
// End csrftoken

let questionTimer;
let answerTimer;
let questionTimeout;
let answerTimeout;
const questionTimeoutToSec = 1000;
const answerTimeoutToSek = 2000;


function showAnswer () {
    $('#answer_text').show();
    $('#stub').hide();
};


function getDemoTask () {
    $.ajax({
        method: 'get',
        headers: {'X-CSRFToken': csrftoken},
        data: $(this).serialize(),
        dataType: 'json',
        success: function (data) {
            $('#question_text').text(data.question_text);
            $('#answer_text').hide();
            $('#stub').show();
            $('#answer_text').text(data.answer_text);
            questionTimeout = data.timeout * questionTimeoutToSec;
            answerTimeout = data.timeout * answerTimeoutToSek;
            questionTimer = setTimeout(getDemoTask, answerTimeout);
            answerTimer = setTimeout(showAnswer, questionTimeout);
        },
    });
};


function clearTaskTimers () {
    clearTimeout(answerTimer);
    clearTimeout(questionTimer);
}


function getNextDemoTaskStep (e) {
    e.preventDefault()
    if ($('#answer_text').css('display') === 'none') {
        // display current task answer
        clearTaskTimers()
        showAnswer();
        questionTimer = setTimeout(getDemoTask, questionTimeout);
    } else {
        // display next task question
        clearTaskTimers();
        getDemoTask();
    }
}


$(document).ready(function () {
    $(function ($) {
        getDemoTask();
        $('#next_task_step').click(getNextDemoTaskStep);
    })
});