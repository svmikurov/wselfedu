$(document).ready(function () {
    $('#word_form').submit(function (e) {
        e.preventDefault();
        $.ajax({
            method: 'post',
            data: $(this).serialize(),
            dataType: 'json',
            success: function (data) {
                $('#message').remove();
                $('#messages').append('<div id="message" class="alert alert-success alert-dismissible fade show" role="alert"></div>');
                $('#message').html(data.success_message);
                $('#message').append('<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>');
                $('#id_foreign_word').val('');
                $('#id_native_word').val('');
                $('#id_foreign_word').focus();
            }
        })
    })
})