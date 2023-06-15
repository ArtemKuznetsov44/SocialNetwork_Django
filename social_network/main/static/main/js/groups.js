// Event handler which works when before page reloading:
$(window).on('beforeupload', function(event) {
    if (!event.persisted) {
        // Этот код будет выполнен только при обычной перезагрузке страницы
        console.log('Hello')
    }
});