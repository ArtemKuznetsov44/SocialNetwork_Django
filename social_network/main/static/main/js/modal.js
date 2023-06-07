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

// When document in ready state:
$(function ($) {

    $('.likes').on('click', function () {
        // var $this = $(this); // Сохраняем ссылку на внешний контекст
        console.log('post_id -', $(this).attr('value'))
        console.log('before likes count - ', $(this).find('div[class="likes_count"]').html())

        let element = $(this).find('div[class="likes_count"]') // Element for update.
        let likes_count = parseInt(element.html()) // Likes count in element like int.

        $.ajax({
            type: 'post',
            url: '/like_ajax/',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            dataType: 'json',
            data: { post_id: $(this).attr('value') },
            success: function (response) {
                if (response.create) {
                    likes_count += 1
                    console.log('after plus', likes_count)
                    element.html(likes_count)
                }
                else {
                    likes_count -= 1
                    console.log('after minus', likes_count)
                    element.html(likes_count)
                }
            },
            error: function (response) {
                console.log('err -', response.responseJSON.error)
            }
        })
        console.log()
    });

    // ================ WORK WITH COMMENTS ================= //
    // When we click on comments ICON:
    $('.comments').on('click', function () {
        console.log($(this).attr('value'))

        $.ajax({
            type: 'post',
            url: '/comment_ajax/',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            dataType: 'json',
            data: { text: 'get_comments', post_id: $(this).attr('value') },
            success: function (response) {
                console.log(response)
                $('form').attr('value', response.post_id)
                
                $('#prev_comments_container').empty()

                for (let i = 0; i < response.comments.length; i++) {

                    // Main comment container:
                    let new_comment_container = $('<div>').addClass('comment-container').css({
                        'display': 'flex',
                        'background-color': '#171717',
                        'border-radius': '10px',
                        'flex-direction': 'column',
                        'padding': '5px',
                        'justify-content': 'center',
                        'align-items': 'flex-start',
                        'margin': '10px',
                        'min-height': '30px',
                    })
                    
                    // User name creation:
                    let username = response.comments[i]['first_name'] + " " + response.comments[i]['last_name'] + ": "
                    // Create the container for user name:
                    let new_comment_user_name = $('<div>').addClass('comment-username').text(username).css({
                        'font-weight': 'bold',
                        'margin-right': '10px',
                        'margin-left': '10px',
                        'border-bottom': '1px solid white',
                    })

                    // Create the container for comment:
                    let new_comment_comment = $('<div>').addClass('comment-comment').text(response.comments[i]['comment']).css({
                        'word-wrap': 'break-word',
                        'margin': '5px 20px 5px 20px'
                    })

                    new_comment_container.append(new_comment_user_name)
                    new_comment_container.append(new_comment_comment)

                    $('#prev_comments_container').append(new_comment_container)
                    new_comment_container.fadeIn(1000)
                }
            },
            error: function (response) {
                console.log('err -', response)
                setTimeout(() => $('#prev_comments_container').text(response.responseJSON.error), 2000);
                $('#add_comment_ajax_form > div.modal-body > label').hide()
                $('form').attr('value', response.responseJSON.post_id)
            }
        })
    });

    // Catch submit event from COMMENT ADDITING modal FORM:
    $('#add_comment_ajax_form').submit(function (e) {
        e.preventDefault()                  // Stop submit default event:
        console.log(this)                   // Print log in console with our form.   

        var csrf_token = $(this).find('input[name="csrfmiddlewaretoken"]').val(); // Получение значения CSRF токена

        $.ajax({
            type: this.method,
            url: this.action,
            headers: { 'X-CSRFToken': csrf_token }, // Передача CSRF токена в заголовке
            dataType: 'json',
            data: { text: 'leave_comment', data: $(this).find('[name="comment"]').val(), post_id: $(this).attr('value') },
            success: function (response) {
                console.log('ok - ', response)
                $(".alert-danger").text('').addClass('d-none')
                $(".alert-success").text(response.ok).removeClass('d-none')
                setTimeout(() => window.location.reload(), 2000);
            },
            error: function (response) {
                console.log('err - ', response)
                $(".alert-success").text('').addClass('d-none')
                $(".alert-danger").text(response.responseJSON.error).removeClass('d-none')
            }
        })
    });

    // ================ END WORK WITH COMMENTS ================= //

    // ================ WORK WITH PHOTOS ================= //

    // Catch submit event from PHOTO ADDITING modal FORM:
    $('#add_photo_ajax_form').submit(function (e) {
        e.preventDefault()                  // Stop submit default event:
        console.log(this)                   // Print log in console with our form.   
        var formData = new FormData(this);  // Create the new FormData object:

        // Add our pictures from form input with id: id_photo into the photoInput list:
        var photoInput = $('#id_photo')[0];

        // Checking that our list has enything in it:
        if (photoInput.files.length > 0) {
            // In success case add our file into FormData object with key like 'photo' (we will use it in our post receiver method):
            formData.append('photo', photoInput.files[0]);
        }
        // Call ajax_send function with prepared params:
        ajax_send(this, formData)
    });

    // ================ END WORK WITH PHOTOS ================= //



    // Catch submit event from POST ADDITING modal FORM:
    $('#add_post_ajax_form').submit(function (e) {
        e.preventDefault()                  // Stop submit default event:
        console.log(this)                   // Print log in console with our form.   
        var formData = new FormData(this);  // Create the new FormData object:

        // Add our content elements from FORM input with id: id_content into the contentInput list:
        var contentInput = $('#id_content')[0];

        // Checking that our list has enything in it:
        if (contentInput.files.length > 0) {
            // In success case add our file into FormData object with key like 'content'
            // (we will use it in our post receiver method):
            formData.append('content', contentInput.files[0]);
        }

        ajax_send(this, formData)  // Call ajax_send function with prepared params:
    });

    $('.one-post-delete-icon').on('click', function (e) {
        
        $.ajax({
            type: 'post', 
            url: '/post_delete_ajax/', 
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            dataType: 'json', 
            data: {post_id: $(this).attr('value')}, 
            success: function(response) {
                console.log('ok -', response.ok)
                window.location.reload()
            }, 
            error: function(response) {
                console.log('err -', response.responseJSON.error)
            }
        })

    }); 

    // ================ END WITH POSTS ================= //
})

// The base body of ajax function:
function ajax_send(form, formData) {
    $.ajax({
        type: form.method,  // Type of request from FORM
        url: form.action,   // URL for sending also from FORM
        processData: false, // Отключаем автоматическую обработку данных
        contentType: false, // Отключаем автоматическое установление типа контента
        dataType: 'json',   // Content type of data for sending below and for repsonse.
        data: formData,     // Data is our formData object (for pictures our anothet not text content):
        success: function (response) {
            console.log('ok - ', response)
            $('.alert-danger').text('').addClass('d-none')
            $(".alert-success").text(response.ok).removeClass('d-none')
            setTimeout(() => window.location.reload(), 2000)
        },
        error: function (response) {
            console.log('err - ', response)
            if (response.status === 400) {
                $(".alert-success").text('').addClass('d-none')
                $('.alert-danger').text(response.responseJSON.error).removeClass('d-none')
            }
        }
    })
}

