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