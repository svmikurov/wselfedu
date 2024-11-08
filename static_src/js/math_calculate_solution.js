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


function getNextTask () {
    $.ajax({
        url: "/math/render-calculate-task/",
        method: 'get',
        data: $(this).serialize(),
        headers: {'X-CSRFToken': csrftoken},
        dataType: 'json',
        success: function (data) {
            $('#question_text').text(data.question_text);
            $('#balance').text(data.balance);
        },
    });
};


$(document).ready(function () {
    $(function ($) {
        getNextTask();

        $('#solution_form').submit(function (e) {
            e.preventDefault()
            $.ajax({
                type: this.method,
                url: this.action,
                data: $(this).serialize(),
                dataType: 'json',
                success: function (data) {
                    let is_correct_solution = data.is_correct_solution;
                    let msg = data.msg;
                    $('#id_user_solution').val('');
                    $('#id_user_solution').focus();
                    $('#evaluation_msg').text(msg);
                    if (is_correct_solution) {
                        getNextTask();
                    };
                }
            })
        })
    })
})
