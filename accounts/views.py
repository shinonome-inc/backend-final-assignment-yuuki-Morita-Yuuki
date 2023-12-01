# from django.shortcuts import render


from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from tweets.models import Like, Tweet

from .forms import SignupForm
from .models import FriendShip

User = get_user_model()


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return response


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = "accounts/user_profile.html"
    model = Tweet
    context_object_name = "tweets"

    def get_queryset(self):
        username = self.kwargs["username"]
        self.user = get_object_or_404(User, username=username)
        return Tweet.objects.select_related("user").prefetch_related("likedtweet").filter(user=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        context["is_following"] = FriendShip.objects.filter(followee=self.user, follower=self.request.user)
        following_count = FriendShip.objects.filter(follower=self.user).count()
        context["following_count"] = following_count
        follower_count = FriendShip.objects.filter(followee=self.user).count()
        context["follower_count"] = follower_count
        context["like_list"] = Like.objects.filter(likeuser=self.request.user).values_list("likedtweet__pk", flat=True)
        return context


class FollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        followee_name = self.kwargs["username"]
        followee = get_object_or_404(User, username=followee_name)

        if request.user == followee:
            return HttpResponseBadRequest("自分自身のユーザーをフォローすることはできません。")
        elif FriendShip.objects.filter(follower=self.request.user, followee=followee).exists():
            return HttpResponseBadRequest("既にフォローしています．")
        else:
            FriendShip.objects.get_or_create(follower=request.user, followee=followee)
            return redirect("accounts:user_profile", username=followee_name)


class UnFollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        followee_name = self.kwargs["username"]
        followee = get_object_or_404(User, username=followee_name)

        if followee == request.user:
            return HttpResponseBadRequest("自分自身のユーザーに操作することはできません。")

        else:
            FriendShip.objects.filter(follower=request.user, followee=followee).delete()

        return redirect("accounts:user_profile", username=followee_name)


class FollowingListView(LoginRequiredMixin, ListView):
    model = FriendShip
    template_name = "accounts/following_list.html"
    context_object_name = "following_list"

    def get_queryset(self):
        username = self.kwargs["username"]
        self.user = get_object_or_404(User, username=username)
        return FriendShip.objects.select_related("followee").filter(follower=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profileuser"] = self.user
        return context


class FollowerListView(LoginRequiredMixin, ListView):
    model = FriendShip
    template_name = "accounts/follower_list.html"
    context_object_name = "follower_list"

    def get_queryset(self):
        username = self.kwargs["username"]
        self.user = get_object_or_404(User, username=username)
        return FriendShip.objects.select_related("follower").filter(followee=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profileuser"] = self.user
        return context
