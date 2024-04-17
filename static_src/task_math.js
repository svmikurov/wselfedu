$(document).ready(function () {
    $(function ($) {
        $('#task_ajax').submit(function (e) {
            e.preventDefault()
            $.ajax({
                type: this.method,
                url: this.action,
                data: $(this).serialize(),
                dataType: 'json',
                success: function (data) {
                    $('#evaluate').text(data.evaluate);
                    $('#task_text').text(data.task_text);
                    $('#id_user_answer').val('');
                }
            })
        })
    })
})