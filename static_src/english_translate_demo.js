import {csrftoken} from './csrf-token.js';

let questionTimer;
let answerTimer;
let questionTimeout;
let answerTimeout;
let knowledge_url;
const questionTimeoutToSec = 1000;
const answerTimeoutToSec = 2000;


function showAnswer () {
    $('#answer_text').show();
    $('#stub').hide();
}


function clearTaskTimers () {
    clearTimeout(answerTimer);
    clearTimeout(questionTimer);
}


function pauseButton () {
    clearTaskTimers();
}


function getDemoTask () {
    $.ajax({
        method: 'post',
        headers: {'X-CSRFToken': csrftoken},
        data: $(this).serialize(),
        dataType: 'json',
        success: function (data) {
            clearTaskTimers();
            // Set question and answer task text
            $('#question_text').text(data.question_text);
            $('#answer_text').hide();
            $('#stub').show();
            $('#answer_text').text(data.answer_text);
            // Set task info
            $('#word_count').text('Выбрано слов: ' + data.word_count);
            $('#knowledge_assessment').text('Уровень: ' + data.knowledge);
            // Set google translate word link
            $('#google-translate').attr('href', data.google_translate_word_link)
            // Set elements attrs and text
            knowledge_url = data.knowledge_url;
            $('#update_favorites').attr('action', data.favorites_url);
            if (data.favorites_status === true) {
                $('#favorites_button').html('Убрать из избранных');
            } else {
                $('#favorites_button').html('Добавить в избранные');
            }
            // Set task timeouts
            questionTimeout = data.timeout * questionTimeoutToSec;
            answerTimeout = data.timeout * answerTimeoutToSec;
            questionTimer = setTimeout(getDemoTask, answerTimeout);
            answerTimer = setTimeout(showAnswer, questionTimeout);
        },
        error: function (data) {
            window.location.href = data.responseJSON.redirect_no_words;
        }
    })
}


function favoritesAction (e) {
    e.preventDefault()
    $.ajax({
        url: this.action,
        type: this.method,
        data: $(this).serialize(),
        dataType: 'json',
        success: function (data) {
            $('#update_favorites').attr('action', data.favorites_url)
            if (data.favorites_status === true) {
                $('#favorites_button').html('Убрать из избранных');
            } else {
                $('#favorites_button').html('Добавить в избранные');
            }
        }
    });
};


function getNextDemoTaskStep (e) {
    e.preventDefault()
    if ($('#answer_text').css('display') === 'none') {
        // display current task answer
        clearTaskTimers();
        showAnswer();
        questionTimer = setTimeout(getDemoTask, questionTimeout);
    } else {
        // display next task question
        clearTaskTimers();
        getDemoTask();
    }
}


function addAssessmentUp (e) {
    e.preventDefault()
    $.ajax({
        url: knowledge_url,
        type: 'post',
        headers: {'X-CSRFToken': csrftoken},
        data: {'assessment': '+1'},
        dataType: 'json',
        success: function (data) {
            getDemoTask();
        }
    })
}


function addAssessmentDown (e) {
    e.preventDefault();
    $.ajax({
        url: knowledge_url,
        type: 'post',
        headers: {'X-CSRFToken': csrftoken},
        data: {'assessment': '-1'},
        dataType: 'json',
        success: function (data) {
            getDemoTask();
        }
    });
}

$(document).ready(function () {
    $(function ($) {
        // Run exercise
        getDemoTask();
        // Set events
        $('#next_task_step').click(getNextDemoTaskStep);
        $('#update_favorites').submit(favoritesAction);
        $('#knowledge_up').click(addAssessmentUp);
        $('#knowledge_down').click(addAssessmentDown);
        $('#pause').click(pauseButton);
    })
});