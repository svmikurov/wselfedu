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

$(document).ready(function () {
    $(function ($) {
        let questionTimer;
        let answerTimer;
        let questionTimeout;
        let answerTimeout;

        function showAnswer () {
            $('#answer_text').show();
            $('#stub').hide();
        };

        function getNextTask () {
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
                    questionTimeout = data.timeout * 1000;
                    answerTimeout = data.timeout * 2000;
                    questionTimer = setTimeout(getNextTask, answerTimeout);
                    answerTimer = setTimeout(showAnswer, questionTimeout);
                },
            });
        };
        getNextTask();

        // Next task state.
        $('#next_task_step').click(function (e) {
            e.preventDefault()
            if ($('#answer_text').css('display') == 'none') {
                clearTimeout(answerTimer);
                clearTimeout(questionTimer);
                showAnswer();
                questionTimer = setTimeout(getNextTask, questionTimeout);
            } else {
                clearTimeout(answerTimer);
                clearTimeout(questionTimer);
                getNextTask();
            }
        });
    })
});