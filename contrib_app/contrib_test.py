from django.contrib.messages import get_messages


def flash_message_test(response, expected_message):
    number_message = 1
    current_message = get_messages(response.wsgi_request)
    assert len(current_message) == number_message
    assert str(*current_message) == expected_message
