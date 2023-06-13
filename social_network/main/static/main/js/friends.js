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

    $('.right-part-head-friends-category').css({
        'background-color': '#404040'
    })

    $('.right-part-head-categories').find('div').hover(function() {
        $(this).css({
            'cursor': 'pointer'
        })
    })

    let friends_container = $('.right-part-body-friends')
    let requests_container = $('.right-part-body-requests')
    let users_container = $('.right-part-body-users')

    $('.right-part-head-friends-category').on('click', function (e) {

        $(this).css({
            'background-color': '#404040'
        })
      
        $('.right-part-head-users-category').css({
            'background-color': '#171717'
        })
        $('.right-part-head-requests-category').css({
            'background-color': '#171717'
        })
        if (!friends_container.hasClass('d-none')) {
            friends_container.addClass('d-none')
        }
        if (requests_container.hasClass('d-none')) {
            requests_container.removeClass('d-none')
        }
        if (!users_container.hasClass('d-none')) {
            users_container.addClass('d-none')
        }

        if (friends_container.hasClass('d-none')) {
            friends_container.removeClass('d-none')
        }
        if (!requests_container.hasClass('d-none')) {
            requests_container.addClass('d-none')
        }
        if (!users_container.hasClass('d-none')) {
            users_container.addClass('d-none')
        }

    })

    $('.right-part-head-requests-category').on('click', function (e) {
        $(this).css({
            'background-color': '#404040'
        })
      
        $('.right-part-head-users-category').css({
            'background-color': '#171717'
        })
        $('.right-part-head-friends-category').css({
            'background-color': '#171717'
        })
        if (!friends_container.hasClass('d-none')) {
            friends_container.addClass('d-none')
        }
        if (requests_container.hasClass('d-none')) {
            requests_container.removeClass('d-none')
        }
        if (!users_container.hasClass('d-none')) {
            users_container.addClass('d-none')
        }
    })

    $('.right-part-head-users-category').on('click', function (e) {
        $(this).css({
            'background-color': '#404040'
        })
       
        $('.right-part-head-requests-category').css({
            'background-color': '#171717'
        })
        $('.right-part-head-friends-category').css({
            'background-color': '#171717'
        })
        if (!friends_container.hasClass('d-none')) {
            friends_container.addClass('d-none')
        }
        if (!requests_container.hasClass('d-none')) {
            requests_container.addClass('d-none')
        }
        if (users_container.hasClass('d-none')) {
            users_container.removeClass('d-none')
        }
    })

    $('.send-request').on('click', function (e) {
        console.log(this)

        send_ajax(this, 'send')
    })

    $('.accept-request').on('click', function (e) {
        console.log(this)

        send_ajax(this, 'accept')
    })

    $('.make-follower').on('click', function (e) {
        console.log(this)

        send_ajax(this, 'make-follower')
    })
})

function send_ajax(object, task) {
    $.ajax({
        type: 'post',
        url: '/request_ajax/',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        dataType: 'json',
        data: { task: task, user_id: $(object).attr('value') },
        success: function (response) {
            console.log('ok -', response)
            window.location.reload()
            $(document).ready(function () {
                $('.right-part-head-users-category').click(function () { // задаем функцию при нажатиии на элемент <button>
                    $('.right-part-head-users-category').click(); // вызываем событие click на элементе <div>
                })
            })

        },
        error: function (response) {
            console.log('err -', response)
        }
    })
}