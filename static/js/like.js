const getCookie = (name) => {
    if (document.cookie && document.cookie !== '') {
        for (const cookie of document.cookie.split(';')) {
            const [key, value] = cookie.trim().split('=')
            if (key === name) {
                return decodeURIComponent(value)
            }
        }
    }
};
const csrftoken = getCookie('csrftoken');

const toggleLike = async (id) => {
    const selector = document.querySelector("#" + id);
    const url = selector.dataset.url;
    const data = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
    }
    const response = await fetch(url, data);
    const tweet_data = await response.json();
    changeStyle(tweet_data, selector);
}

const changeStyle = (tweet_data, selector) => {
    const likes_count = document.querySelector("#likes_count_" + tweet_data.tweet_id)
    if (tweet_data.liked) {
        unlike_url = tweet_data.unlike_url;
        selector.setAttribute('data-url', unlike_url);
        selector.innerHTML = "いいね取り消し";
        likes_count.textContent = tweet_data.likes_count + "いいね";
    } else {
        like_url = tweet_data.like_url;
        selector.setAttribute('data-url', like_url);
        selector.innerHTML = "いいね";
        likes_count.textContent = tweet_data.likes_count + "いいね";
    }
}
