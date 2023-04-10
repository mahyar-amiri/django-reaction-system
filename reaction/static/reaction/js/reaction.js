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

function load(element, url) {
    let xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
    }

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState === XMLHttpRequest.DONE) {
            if (xmlhttp.status === 200) {
                element.innerHTML = xmlhttp.responseText;
                const allScripts = element.getElementsByTagName('script');
                for (let n = 0; n < allScripts.length; n++) {
                    eval(allScripts [n].innerHTML)//run script inside div generally not a good idea but these scripts are anyways intended to be executed.
                }
            } else {
                alert('Error');
            }
        }
    }

    xmlhttp.open('GET', url, true);
    xmlhttp.send();
}

function React(urlhash, react_slug) {
    let form = document.querySelector(`#form-reaction-${urlhash}`);
    let method = form.getAttribute('method');
    let action = form.getAttribute('action');
    let data = {
        //OBJECT INPUTS
        urlhash,
        react_slug
    };

    // AJAX
    let http = new XMLHttpRequest();
    http.open(method, action, true);

    http.setRequestHeader('Content-type', 'application/json');
    http.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    http.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

    http.onreadystatechange = function () {
        if (http.readyState === XMLHttpRequest.DONE) {
            if (http.status === 200) {
                load(
                    document.querySelector(`#form-reaction-${urlhash}`),
                    `/reaction/react?urlhash=${urlhash}`
                );
            } else {
                alert('ERROR in Submitting Reaction!')
            }
        }
    }
    http.send(JSON.stringify(data));
    // $.ajax({
    //     type: method,
    //     url: action,
    //     data: {
    //         urlhash,
    //         react_slug
    //     },
    //     headers: {
    //         'X-Requested-With': 'XMLHttpRequest',
    //         'X-CSRFToken': getCookie('csrftoken'),
    //     },
    //     success: function () {
    //         load(
    //             document.querySelector(`#form-reaction-${urlhash}`),
    //             `/reaction/react?urlhash=${urlhash}`
    //         );
    //     },
    //     error: function () {
    //         alert('ERROR in Submitting Reaction!')
    //     }
    // });
}

document.addEventListener("DOMContentLoaded", () => {
    const reaction_items = document.querySelectorAll(`[id^='form-reaction-']`)
    reaction_items.forEach(function (item) {
        const urlhash = item.id.replace('form-reaction-', '')
        load(
            document.querySelector(`#form-reaction-${urlhash}`),
            `/reaction/react?urlhash=${urlhash}`
        );
    })
});