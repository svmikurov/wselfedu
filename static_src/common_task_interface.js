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
        var questionTimer;
        var answerTimer;

        function showAnswer () {
            $('#answer_text').show();
        };
        answerTimer = setTimeout(showAnswer, 2000);

        function getNextTask () {
            $.ajax({
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                url: '/common-task-interface/',
                data: $(this).serialize(),
                dataType: 'json',
                success: function (data) {
                    $('#question_text').text(data.task.question_text);
                    $('#answer_text').hide();
                    $('#answer_text').text(data.task.answer_text);
                    answerTimer = setTimeout(showAnswer, 2000);
                    questionTimer = setTimeout(getNextTask, 4000);
                },
            });
        };
        questionTimer = setTimeout(getNextTask, 4000);
    })
});