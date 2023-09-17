from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Tweet

User = get_user_model()


class TestHomeView(TestCase):
    def setUp(self):
        self.url = reverse("tweets:home")
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")
        Tweet.objects.create(user=self.user, content="text1")
        Tweet.objects.create(user=self.user, content="text2")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        test_list = response.context["tweets"]
        tweet_db = Tweet.objects.all()
        self.assertQuerysetEqual(test_list, tweet_db)


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.url = reverse("tweets:create")
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_success_post(self):
        valid_data = {
            "content": "test_content",
        }
        first_tweet_count = Tweet.objects.count()
        response = self.client.post(self.url, valid_data)
        self.assertRedirects(response, reverse("tweets:home"), status_code=302, target_status_code=200)
        self.assertEqual(Tweet.objects.count(), first_tweet_count + 1)
        self.assertTrue(Tweet.objects.filter(content=valid_data["content"]).exists())

    def test_failure_post_with_empty_content(self):
        invalid_data = {"content": ""}
        first_tweet_count = Tweet.objects.count()
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tweet.objects.count(), first_tweet_count)
        self.assertIn("このフィールドは必須です。", form.errors["content"])

    def test_failure_post_with_too_long_content(self):
        invalid_data = {"content": "a" * 301}
        first_tweet_count = Tweet.objects.count()
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tweet.objects.count(), first_tweet_count)
        self.assertIn("この値は 300 文字以下でなければなりません( 301 文字になっています)。", form.errors["content"])


class TestTweetDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")
        self.tweet = Tweet.objects.create(user=self.user, content="test_content")
        self.url = reverse("tweets:detail", args=[str(self.tweet.id)])
        self.post_data = {"content": "test_tweet"}

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        tweet_context = response.context["object"]
        self.assertEqual(tweet_context, self.tweet)


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="testpassword1")
        self.client.login(username="user1", password="testpassword1")
        self.tweet = Tweet.objects.create(user=self.user1, content="test_content")
        self.url = reverse("tweets:delete", args=[str(self.tweet.id)])
        self.post_data = {"content": "test_tweet"}

    def test_success_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tweets:home"), status_code=302, target_status_code=200)
        self.assertFalse(Tweet.objects.filter(id=self.tweet.id).exists())

    def test_failure_post_with_not_exist_tweet(self):
        non_existent_tweet_id = self.tweet.id + 1
        self.url = reverse("tweets:delete", args=[str(non_existent_tweet_id)])
        first_tweet_count = Tweet.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Tweet.objects.count(), first_tweet_count)

    def test_failure_post_with_incorrect_user(self):
        self.another_user = User.objects.create_user(username="user2", password="testpassword2")
        self.client.login(username="user2", password="testpassword2")
        self.url = reverse("tweets:delete", args=[str(self.tweet.id)])
        first_tweet_count = Tweet.objects.count()

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Tweet.objects.count(), first_tweet_count)


# class TestLikeView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_liked_tweet(self):


# class TestUnLikeView(TestCase):

#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_unliked_tweet(self):
