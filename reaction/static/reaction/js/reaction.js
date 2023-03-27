function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function LoadReactions(urlhash) {
    $(`#form-reaction-${urlhash}`).load(
        `/reaction/react?urlhash=${urlhash}`
    );
}

function React(urlhash, react_slug) {
    let form = $(`#form-reaction-${urlhash}`);
    let method = form.prop('method');
    let action = form.prop('action');
    $.ajax({
        type: method,
        url: action,
        data: {
            urlhash,
            react_slug
        },
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: function () {
            LoadReactions(urlhash);
        },
        error: function () {
            alert('ERROR in Reaction!')
        }
    });
}

$(document).ready(function () {
    $('[id^="form-reaction-"]').each(function () {
        LoadReactions(this.id.replace('form-reaction-', ''));
    })
});
