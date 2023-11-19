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
console.log(csrftoken);

function toggleLike(tweet_id) {
    //var csrftoken = getCookie('csrftoken');
    const url = "http://localhost:8000/tweets/" + tweet_id + "/like/";
    //const formData = new FormData();
    //formData.append('csrfmiddlewaretoken', csrftoken);
    console.log(csrftoken);

    fetch(url, {
        method: "POST",
        //mode: "no-cors",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        //credentials: "include",
    })
        .then(response => response.json())
        .then(data => {
            const counter = document.getElementById('like_count' + tweet_id);
            counter.textContent = data.likes_count + '件のいいね';
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
