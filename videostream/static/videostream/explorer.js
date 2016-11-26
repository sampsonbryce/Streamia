console.log('LOADED JS');
$(function(){
    console.log('mapping click');
    initializeButtonClicks()
});

function initializeButtonClicks(){
    $('.load-link').click(getSubDir);
}

function getSubDir(e) {
    console.log('link clicked');
    e.preventDefault();
    var el = $(this);

    $.ajax({
        url: '/videostream/getChildren/',
        type: 'POST',
        data: {'url_prefix': el.attr('data-url')},
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        success: function (data) {
            console.log('result', data);
            el.after(data);
            initializeButtonClicks();
        },
        error: function () {
            alert('error getting children')
        }
    });
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}