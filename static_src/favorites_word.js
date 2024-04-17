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


$(document).ready(function () {
    $(function ($) {
        function showAnswer () {
            $('#task_answer').show();
        };
        setTimeout(showAnswer, 5000);

        function getTask () {
            $.ajax({
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                url: '/english/word-study-ajax/',
                data: $(this).serialize(),
                dataType: 'json',
                success: function (data) {
                    $('#knowledge_assessment').text('Уровень: ' + data.knowledge_assessment);
                    $('#word_count').text('Выбрано слов: ' + data.task.word_count);
                    $('#source').text('Источник: ' + data.task.source);
                    $('#task_question').text(data.task.question);
                    $('#task_answer').hide();
                    $('#task_answer').text(data.task.answer);
                    setTimeout(showAnswer, 5000);
                },
            });
        };
        setInterval(getTask, 10000);

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
            })
        });
    })
})