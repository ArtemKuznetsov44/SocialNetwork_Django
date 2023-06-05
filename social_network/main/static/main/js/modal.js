$(function($) {
    $(document).on('beforeSubmit', '#add_photo_ajax_form', function(e) {
        e.preventDefault()
        console.log(this)

        $.ajax({
            // Type and url we will take from our form with this operator:
            type: this.method, // Our form user POST and here will be the same type:
            url: this.url, // Our form has an action attribute, we can use it here (it were we sill recieve the data):
            data: $(this).serialize(), // Data - data from form after serialization
            dataType: "json", // DataType - we will use jason like in 99% cases
            // This function will be used when we will get the success code of operation from our server:
            success: function(response) {
                console.log('ok - ', response);
                //console.log(window.location);
                $('#ajax_add_photo').modal('hide');
                $.pjax.reload('#pjax-container');
                alert('Hello')
            },
            // This function will be used when we will get the error code of operation from our server:
            // In case when we will get the success response from our server:
            error: function(response) {
                console.log('err -', response)
                if (response.status === 400) {
                    $('#text').text(response.responseJson.error)
                    $('#alert').removeClass('d-none')
                }
            }
        });
    })
})