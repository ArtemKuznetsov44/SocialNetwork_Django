$(function($) {
    let patterns = {
        'email' : /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/, 
        'names': /^[A-Z][a-z]{1,15}$/, 
        'phone': /^\+7-9\d{2}-\d{3}-\d{2}-\d{2}$/, 
        'password': /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=[\]{};':"|,.<>/?]).{8,}$/
    }
      
    $('#id_first_name').on('change', function(e) {
        check_and_response("Your First Name is not valid.", this, patterns['names'])
    })

    $('#id_last_name').on('change', function(e) {
        check_and_response("Your Last Name is not valid.", this, patterns['names'])
    })

    $('input[type="text"][name="username"]').on('change',function(e) {
        
        if (!($.trim($('#id_username').val()).length > 8 ? true : false)) {
            show_error(this, message='Your Username is not valid.')
        }
        else {
            hide_error(this)
        }
    })
    // This is for SIGN IN form: 
    $('input[type="email"][name="username"]').on('change',function(e) {
        check_and_response("Your E-mail is not valid!", this, patterns['email'])
    })

    // This is for REGISTRAION form:
    $('input[type="email"][name="email"]').on('change',function(e) {
        check_and_response("Your E-mail is not valid!", this, patterns['email'])
    })

    $('#id_phone').on('change',function(e) {
        check_and_response("Your Phone is not valid!", this, patterns['phone'])
    })

    $('#id_date_of_birth').on('change',function(e) {
        let input_date_str = $.trim($('#id_date_of_birth').val())
        let input_date = Date.parse(input_date_str)
      
        if (!(input_date > new Date(1920, 1, 1) & input_date <= Date.now() ? true : false)) {
            show_error(this, 'Your Date of Birth is not valid!')
        }
        else {
            hide_error(this)
        }

    })

    $('#id_password').on('change', function (e) {
        check_and_response("You password specified in inccorect format.", this, patterns['password']) 
    }); 
    
    $('#id_password1').on('change', function (e) {
        check_and_response("You password specified in inccorect format.", this, patterns['password']) 
    }); 
})

function check_and_response(message, current_object, pattern) {
    // In case when value does not match with pattern:
    if (!pattern.test($(current_object).val())){
        show_error(current_object, message)
        return false
    }

    hide_error(current_object)
    return true
}

function show_error(object, message) {
    $(object).val('')
    $(object).css({
        'border': '3px solid #F8D7DA'
    })
    $(object).next('.error-for-field').find('div[class="error-msg"]').text(message)
    $(object).next('.error-for-field').removeClass('d-none')
}

function hide_error(object) {
     // In an oposite cas: 
     $(object).css({
        // Bring border to default stiles:
        'border': "var(--bs-border-width) solid var(--bs-border-color)"
    })
    // Errase text from error alert under field and make it invisible with 'd-none' class:
    $(object).next('.error-for-field').find('div[class="error-msg"]').text('')
    $(object).next('.error-for-field').addClass('d-none')
}
