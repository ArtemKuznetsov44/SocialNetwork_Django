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

                    $('#prev_comments_container').append(new_comment_container).fadeIn(1000)

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
        // In success case add our file into FormData object with key like 'photo' (we will use it in our post receiver method):
        formData.append('photo', photoInput.files.length > 0 ? photoInput.files[0] : '');

        // Call ajax_send function with prepared params:
        ajax_send(this, formData)
    });

    // ================ END WORK WITH PHOTOS ================= //

    // ================== WORK WITH POSTS ==================== //

    // Catch submit event from POST ADDITING modal FORM:
    $('#add_post_ajax_form').submit(function (e) {
        e.preventDefault()                  // Stop submit default event:
        console.log(this)                   // Print log in console with our form.   
        var formData = new FormData(this);  // Create the new FormData object:

        // Add our content elements from FORM input with id: id_content into the contentInput list:
        var contentInput = $('#id_content')[0];

        // Checking that our list has enything in it:
        // In success case add our file into FormData object with key like 'content'
        // (we will use it in our post receiver method):
        formData.append('content', contentInput.files.length > 0 ? contentInput.files[0] : '');

        ajax_send(this, formData)  // Call ajax_send function with prepared params:
    });

    $('.one-post-delete-icon').on('click', function (e) {
        e.preventDefault();
        let result = confirm("Are you really whant to delete this post?");

        if (result) {
            $.ajax({
                type: 'post',
                url: '/post_delete_ajax/',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                dataType: 'json',
                data: { post_id: $(this).attr('value') },
                success: function (response) {
                    console.log('ok -', response.ok)
                    window.location.reload()
                },
                error: function (response) {
                    console.log('err -', response.responseJSON.error)
                }
            })
        }
    });

    $('.delete-friend').on('click', function (e) {
        e.preventDefault()

        if (confirm("Are you really whant to delete this user from your friends?"))
            send_ajax('delete-friend', this);

        if (confirm("Do you what to delete this user from your followers?"))
            send_ajax('delete-follower', this);

        function send_ajax(task, object) {
            $.ajax({
                type: 'get',
                url: '/delete_frind_ajax/',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                dataType: 'json',
                data: { task: task, user_id: $(object).attr('value') },
                success: function (resposne) {
                    console.log('ok -', resposne)
                },
                error: function (resposne) {
                    console.log('err -', resposne)
                }
            })
        }
    })

    $('.one-photo-delete-icon').on('click', function (e) {
        e.preventDefault()

        let result = confirm("Are you really whant to delete this photo?");

        if (result) {
            $.ajax({
                type: 'post',
                url: '/photo_delete_ajax/',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                dataType: 'json',
                data: { photo_id: $(this).attr('value') },
                success: function (response) {
                    console.log('ok -', response.ok)
                    window.location.reload()
                },
                error: function (response) {
                    console.log('err -', response.responseJSON.error)
                }
            });
        }
    })

    // ================ END WITH POSTS ================= //

    // ================ WORK WITH PROFILE ============== //
    $('#profile_edit').on('click', function () {
        console.log("Editing")
        $('.modal-body').find('.error-for-field').addClass('d-none')
        $('.modal-body').find('input').css({
            'border': 'var(--bs-border-width) solid var(--bs-border-color)'
        })

        $.ajax({
            type: 'get',
            url: '/profile_edit_ajax/',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            dataType: 'json',
            success: function (response) {
                console.log('ok -', response)
                let inputs = {} // Declare the dictionary:
                // Each is the function for make iterations for elements.
                // Make the loop to fill inputs dictionary where key - name of input and value is the jQuery input element:
                $('.modal-body').find('input').each(function () {
                    // If we use only this we will get the Dom element, but we need jQuery element, thats is why $(this)
                    inputs[$(this).attr('name')] = $(this)
                })
                // Loop to fill all inputs with values from response taken by keys: 
                $.each(response, function (key, value) {
                    if (inputs[key]) {
                        inputs[key].val(value)
                    }
                })
                // Fill select element:
                $('.modal-body').find('select[name="gender"]').val(response['gender'])
            },
            error: function (response) {
                console.log('err -', response)
                $(".alert-danger").text(response.responseJSON.error).removeClass('d-none')
            }
        })
    })

    $('#profile_edit_ajax_form').submit(function (e) {
        e.preventDefault()  // Stop submit default event:
        console.log(this)

        var formData = new FormData(this);  // Create the new FormData object:

        // Add our content elements from FORM input with id: id_content into the contentInput list:
        var profile_img = $('#id_profile_img')[0];
        var profile_back = $('#id_profile_back_img')[0];

        formData.append('profile_img', profile_img.files.length > 0 ? profile_img.files[0] : '');
        formData.append('profile_back_img', profile_back.files.length > 0 ? profile_back.files[0] : '');

        ajax_send(this, formData)
    })

    $('.go-to-dialog').on('click', function (e) {
        console.log(this)

        $.ajax({
            type: 'post',
            url: '/start_dialog_ajax/',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            dataType: 'json',
            data: { user_id: $(this).attr('value') },
            success: function (response) {
                window.location.replace('/messenger/dialog=' + response.ok)
            },
            error: function (response) {
                console.log(response.error)
            }
        })
    })

    document.getElementById("sign-out").addEventListener('click', function (event) {
        event.preventDefault();

        let result = confirm("Are you really what to sign out?");

        if (result) {
            window.location.href = event.target.href;
        }
    })
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
// Event before window reloading:
window.addEventListener('beforeunload', function () {
    // scrollY - property which returns the scroll on Y value. 
    // scrollTop - the same thing, but it works with elemenets on page.

    // Save in localStorege the value of scrollTop property (values in localScrorage we can use after page roloadin):
    this.localStorage.setItem('scrollPosition', document.querySelector(".right-part").scrollTop)
})
// Event in time when page is loading:
window.addEventListener('load', function () {
    // Getting item from localStorage:
    let scrollPosition = this.localStorage.getItem('scrollPosition');
    // If it is not null:
    if (scrollPosition !== null) {
        // Find interesting element and make scrooll to (xPosition, yPosition).
        // yPosition is the value from localStorage. 
        this.document.querySelector(".right-part").scrollTo(0, scrollPosition);
        this.localStorage.removeItem('scrollPosition')
    }
})