from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse

from mysite.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
from tweets.models import Tweet

from .models import FriendShip

User = get_user_model()


class TestSignupView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_success_post(self):
        valid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, valid_data)

        self.assertRedirects(
            response,
            reverse(LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )

    def test_failure_post_with_empty_form(self):
        invalid_data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(User.objects.filter(username=invalid_data["email"]).exists())
        self.assertFalse(User.objects.filter(username=invalid_data["password1"]).exists())
        self.assertFalse(User.objects.filter(username=invalid_data["password2"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["username"])
        self.assertIn("このフィールドは必須です。", form.errors["email"])
        self.assertIn("このフィールドは必須です。", form.errors["password1"])
        self.assertIn("このフィールドは必須です。", form.errors["password2"])

    def test_failure_post_with_empty_username(self):
        invalid_data = {
            "username": "",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["username"])

    def test_failure_post_with_empty_email(self):
        invalid_data = {
            "username": "testuser",
            "email": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["email"])

    def test_failure_post_with_empty_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["password1"])
        self.assertIn("このフィールドは必須です。", form.errors["password2"])

    def test_failure_post_with_duplicated_user(self):
        User.objects.create_user(username="testuser", password="testpassword")
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("同じユーザー名が既に登録済みです。", form.errors["username"])

    def test_failure_post_with_invalid_email(self):
        invalid_data = {
            "username": "testuser",
            "email": "test1",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(
                username=invalid_data["username"],
            ).exists()
        )
        self.assertFalse(form.is_valid())
        self.assertIn("有効なメールアドレスを入力してください。", form.errors["email"])

    def test_failure_post_with_too_short_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "test",
            "password2": "test",
        }

        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このパスワードは短すぎます。最低 8 文字以上必要です。", form.errors["password2"])

    def test_failure_post_with_password_similar_to_username(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testuser",
            "password2": "testuser",
        }

        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このパスワードは ユーザー名 と似すぎています。", form.errors["password2"])

    def test_failure_post_with_only_numbers_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "111111111",
            "password2": "111111111",
        }

        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このパスワードは数字しか使われていません。", form.errors["password2"])

    def test_failure_post_with_mismatch_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassward",
        }

        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("確認用パスワードが一致しません。", form.errors["password2"])


class TestLoginView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:login")
        self.user = User.objects.create_user(username="username", password="password")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_success_post(self):
        valid_data = {
            "username": "username",
            "password": "password",
        }
        response = self.client.post(self.url, valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertIn(SESSION_KEY, self.client.session)
        self.assertRedirects(response, reverse(LOGIN_REDIRECT_URL), status_code=302, target_status_code=200)

    def test_failure_post_with_not_exists_user(self):
        invalid_data = {
            "username": "Notexist",
            "password": "password",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertIn("正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。", form.errors["__all__"])

    def test_failure_post_with_empty_password(self):
        invalid_data = {
            "username": "username",
            "password": "",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertIn("このフィールドは必須です。", form.errors["password"])


class TestLogoutView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpasseord")
        self.url = reverse("accounts:logout")

    def test_success_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse(LOGOUT_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertEqual(response.status_code, 302)


class TestUserProfileView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.another_user = User.objects.create_user(username="anotheruser", password="testpassword")

        Tweet.objects.create(user=self.user, content="test1")
        Tweet.objects.create(user=self.user, content="test2")
        Tweet.objects.create(user=self.another_user, content="anothertest1")
        self.url = reverse("accounts:user_profile", args=["testuser"])
        FriendShip.objects.create(follower=self.user, followee=self.another_user)

        self.client.login(username="testuser", password="testpassword")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        user_context = response.context["user"]
        tweets_context = response.context["tweets"]
        user_db = User.objects.get(username="testuser")
        tweets_db = Tweet.objects.filter(user=user_db)

        follower_count_context = response.context["follower_count"]
        followee_count_context = response.context["following_count"]
        follower_count_db = FriendShip.objects.filter(followee=self.user).count()
        followee_count_db = FriendShip.objects.filter(follower=self.user).count()

        self.assertEqual(user_context, user_db)
        self.assertQuerysetEqual(tweets_context, tweets_db, ordered=False)
        self.assertEqual(follower_count_context, follower_count_db)
        self.assertEqual(followee_count_context, followee_count_db)


# class TestUserProfileEditView(TestCase):


#     def test_success_post(self):

#      def test_failure_post_with_not_exists_user(self):

#     def test_failure_post_with_incorrect_user(self):


class TestFollowView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.another_user = User.objects.create_user(username="anotheruser", password="testpassword")
        self.url = reverse("accounts:follow", kwargs={"username": self.another_user.username})
        self.client.login(username="testuser", password="testpassword")

    def test_success_post(self):
        FriendShip.objects.create(follower=self.user, followee=self.another_user)
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse("accounts:user_profile", kwargs={"username": self.another_user}),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(FriendShip.objects.filter(follower=self.user).exists())

    def test_failure_post_with_not_exist_user(self):
        nonexistent_username = "nonexistentuser"
        self.url = reverse("accounts:follow", kwargs={"username": nonexistent_username})
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

        self.assertFalse(FriendShip.objects.filter(follower=self.user).exists())

    def test_failure_post_with_self(self):
        self.url = reverse("accounts:follow", kwargs={"username": self.user})
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(FriendShip.objects.filter(follower=self.user).exists())


class TestUnfollowView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.another_user = User.objects.create_user(username="anotheruser", password="testpassword")
        self.url = reverse("accounts:unfollow", kwargs={"username": self.another_user.username})
        self.client.login(username="testuser", password="testpassword")
        FriendShip.objects.create(follower=self.user, followee=self.another_user)

    def test_success_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse("accounts:user_profile", kwargs={"username": self.another_user}),
            status_code=302,
            target_status_code=200,
        )
        self.assertFalse(FriendShip.objects.filter(follower=self.user).exists())

    #     def test_failure_post_with_not_exist_tweet(self):

    def test_failure_post_with_incorrect_user(self):
        nonexistent_username = "nonexistentuser"
        self.url = reverse("accounts:follow", kwargs={"username": nonexistent_username})
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(FriendShip.objects.filter(follower=self.user).exists())

    def test_failure_post_with_self(self):
        self.url = reverse("accounts:unfollow", kwargs={"username": self.user})
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 400)
        self.assertTrue(FriendShip.objects.filter(follower=self.user).exists())


class TestFollowingListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.another_user = User.objects.create_user(username="anotheruser", password="testpassword")
        self.url = reverse("accounts:following_list", kwargs={"username": self.user.username})
        self.client.login(username="testuser", password="testpassword")
        FriendShip.objects.create(follower=self.user, followee=self.another_user)

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestFollowerListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.another_user = User.objects.create_user(username="anotheruser", password="testpassword")
        self.url = reverse("accounts:follower_list", kwargs={"username": self.user.username})
        self.client.login(username="testuser", password="testpassword")
        FriendShip.objects.create(follower=self.user, followee=self.another_user)

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
