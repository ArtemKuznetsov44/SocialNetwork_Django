$(function ($) {
    $('#reg_form').submit(function (e) {
        // e.preventDefault()
        $.ajax({
            // Type and url we will take from our form with this operator:
            type: this.method,
            url: this.url,
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                console.log(responce)
            }, 
            // In case when we will get the success response from our server:
            error: function (responce) {
                console.log(responce)
            }
        });
    })
})