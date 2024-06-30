$(document).ready(function () {
    $(function ($) {
        // https://api.jquery.com/attribute-starts-with-selector/
        $("form[id^='update_favorites']").submit(function (e) {
            var wordId = $(this).attr('data-word-id');
            e.preventDefault();
            $.ajax({
                type: this.method,
                url: this.action,
                data: $(this).serialize(),
                dataType: 'json',
                success: function (data) {
                    if (data.favorites_status === true) {
                        $('#favorites_button_' + wordId).html('Убрать');
                    } else {
                        $('#favorites_button_' + wordId).html('Добавить');
                    }
                }
            });
        })
    })
})