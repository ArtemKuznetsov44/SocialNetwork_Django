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

$(function ($) {
    $('.right-part-body-main').scrollTop($('.right-part-body-main').height())
    let chat_id = $('svg').attr('dialog')

    $('#send-message').on('click', function (e) {
        console.log(this)

        let message = ($('textarea').val())
        $('textarea').val('')
        $.ajax({
            type: 'post',
            url: '/message_ajax/',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            dataType: 'json',
            data: { sender_id: $(this).attr('sender'), chat: chat_id, message: message },
            success: function (response) {
                console.log('ok -', response.ok)
            },
            error: function (response) {
                console.log('err -', response.responseJSON.error)
            }

        })
    })

    // $("#myElement").scrollTop($("#myElement").scrollHeight);
    setInterval(function () {
        let last_msg_element = $('.right-part-body-main .one-message:last');
        let last_msg_id = last_msg_element.length > 0 ? last_msg_element.attr('value') : "";

        console.log(last_msg_id)
        $.ajax({
            type: 'get',
            url: '/message_ajax/',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            dataType: 'json',
            data: { last_msg_id: last_msg_id, chat_id: chat_id },
            success: function (response) {
                console.log('ok - ', response.ok)

                if (response.ok != '') {
                    let one_message_container = $('<div>').addClass('one-message').attr('value', response.ok['pk'])

                    let one_message_info_container = $('<div>').addClass('one-message-info')

                    let username = response.ok['sender_first_name'] + " " + response.ok['sender_last_name']

                    let user_name_container = $('<div>').addClass('user-name').text(username)

                    let message_time_container = $('<div>').addClass('message-time').text(response.ok['sent_at'])

                    let message_body_container = $('<div>').addClass('message-body').text(response.ok['text'])

                    one_message_info_container.append(user_name_container)
                    one_message_info_container.append(message_time_container)

                    one_message_container.append(one_message_info_container)
                    one_message_container.append(message_body_container)

                    $('.right-part-body-main').append(one_message_container)
                    document.querySelector(".right-part-body-main").scrollTo(0, document.querySelector(".right-part-body-main").scrollHeight)
                }
            },
            error: function (response) {
                console.log('error -', response.responseJSON.error)
            }
        })
    }, 2000)

})