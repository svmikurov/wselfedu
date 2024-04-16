$(document).ready(function () {
    $(function ($) {
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
        })
    })
})