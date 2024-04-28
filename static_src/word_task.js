// csrftoken
// https://docs.djangoproject.com/en/5.0/howto/csrf/#using-csrf-protection-with-ajax
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

const outlineStateClass = "btn btn-outline-primary btn-sm";


$(document).ready(function () {
    $(function ($) {
        var answerTimer;
        var questionTimer;
        var task_status;

        function showAnswer () {
            $('#task_answer').show();
        };
        answerTimer = setTimeout(showAnswer, 5000);

        function getTask () {
            $.ajax({
                method: 'POST',
                // https://docs.djangoproject.com/en/5.0/howto/csrf/#setting-the-token-on-the-ajax-request
                headers: {'X-CSRFToken': csrftoken},
                url: '/task/word-study-ajax/',
                data: $(this).serialize(),
                dataType: 'json',
                success: function (data) {
                    $('#google-translate').attr('href', data.task.google_translate_word_link);
                    $('#knowledge_action_url').attr('action', data.task.knowledge_action_url);
                    $('#knowledge_assessment').text('Уровень: ' + data.knowledge_assessment);
                    $('#word_count').text('Выбрано слов: ' + data.task.word_count);
                    $('#source').text('Источник: ' + data.task.source);
                    $('#task_question').text(data.task.question);
                    $('#task_answer').hide();
                    $('#task_answer').text(data.task.answer);
                    // Favorites word button
                    $('#favorites_button').html('');
                    if (data.favorites_status === true) {
                        $('#favorites_button').html('Убрать из избранных');
                    } else {
                        $('#favorites_button').html('Добавить в избранные');
                    };// End Favorites word button
                    answerTimer = setTimeout(showAnswer, 5000);
                    questionTimer = setTimeout(getTask, 10000);
                },
            });
        };
        questionTimer = setTimeout(getTask, 10000);

        // Favorites word action.
        $('#update_favorites').submit(function (e) {
            e.preventDefault()
            $.ajax({
                type: this.method,
                url: this.action,
                data: $(this).serialize(),
                dataType: 'json',
                success: function (data) {
                    if (data.favorites_status === true) {
                        $('#favorites_button').html('Убрать из избранных');
                    } else {
                        $('#favorites_button').html('Добавить в избранные');
                    }
                }
            });
        });

        // Next task state.
        $('#next_task_step').click(function (e) {
            e.preventDefault()
            if ($('#task_answer').css('display') == 'none') {
                clearTimeout(answerTimer);
                clearTimeout(questionTimer);
                showAnswer();
                questionTimer = setTimeout(getTask, 5000);
            } else {
                clearTimeout(answerTimer);
                clearTimeout(questionTimer);
                getTask();
            }
        });
    })
})