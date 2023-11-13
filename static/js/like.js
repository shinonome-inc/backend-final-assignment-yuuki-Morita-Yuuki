function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function toggleLike(id) {
    const selector = document.getElementById(id);
    if (selector && selector.dataset.url) {
        const url = selector.dataset.url;
        console.log(url);
    } else {
        console.error('Error: Element not found or data-url attribute is missing.');
        return;
    }

    fetch(url, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({}),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const counter = document.getElementById('like_count');
            counter.textContent = data.likes_count + '件のいいね';

            updateStyleBasedOnLikeStatus(data.is_liked, selector);
        })
        .catch(error => {
            console.error('Error:', error);
        });


    function updateStyleBasedOnLikeStatus(isLiked, selector) {
        if (isLiked) {
            const unlike_url = tweet_data.unlike_url;
            selector.setAttribute('data-url', unlike_url);
            selector.innerHTML = "いいね取り消し";
        } else {
            const like_url = tweet_data.like_url;
            selector.setAttribute('data-url', like_url);
            selector.innerHTML = "いいね";
        }
    }

    toggleLike('like-post');
}
