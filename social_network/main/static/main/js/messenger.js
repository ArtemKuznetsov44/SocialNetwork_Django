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

$(function($){
    $('.go-to-dialog').on('click', function(e) {
        console.log(this)

        $.ajax({
            type: 'post',
            url: '/start_dialog_ajax/',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            dataType: 'json',
            data: {user_id : $(this).attr('value')}, 
            success: function(response) {
                window.location.replace('/messenger/dialog=' + response.ok )
            },
            error: function(response){
                console.log(response.error)
            }
        })
    })
})