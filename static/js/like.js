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

function updateLikesCount(tweetId) {
    var likeCountSpan = $("#likes_count_" + tweetId);
    var likeCountUrl = "/tweets/get_likes_count/" + tweetId + "/";


    $.ajax({
        type: "GET",
        url: likeCountUrl,
        dataType: "json",
        success: function (response) {
            if (response.likes_count !== undefined) {
                likeCountSpan.text(response.likes_count + " いいね数");
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
}


function toggleLike(tweetId) {
    var likeButton = $("#" + tweetId);
    var likeCountSpan = $("#likes_count_" + tweetId);
    var likeUrl = likeButton.data("url");
    $.ajax({
        type: "POST",
        url: likeUrl,
        dataType: "json",
        success: function (response) {


            likeCountSpan.text(response.likes_count + " いいね数");

            if (likeButton.text() === "いいね") {
                likeButton.text("いいね取り消し");
                likeButton.data("url", likeUrl.replace('/like/', '/unlike/'));
            } else {
                likeButton.text("いいね");
                likeButton.data("url", likeUrl.replace('/unlike/', '/like/'));
            }
        },
        error: function (error) {
            console.log(error);
            console.log("Ajax error:", error);
        }
    });
}



$(document).ready(function () {
    var tweetIds = $(".like-button").map(function () {
        return this.id;
    }).get();

    tweetIds.forEach(function (tweetId) {
        updateLikesCount(tweetId);
    });
});
