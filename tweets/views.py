# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView
from django.views.generic.list import ListView

from .models import Like, Tweet


class HomeView(LoginRequiredMixin, ListView):
    template_name = "tweets/home.html"
    model = Tweet
    context_object_name = "tweets"
    queryset = model.objects.select_related("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["like_list"] = Like.objects.filter(likeuser=self.request.user).values_list("likedtweet__pk", flat=True)
        return context


class TweetCreateView(LoginRequiredMixin, CreateView):
    model = Tweet
    template_name = "tweets/tweets_create.html"
    success_url = reverse_lazy("tweets:home")
    fields = ["content"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = Tweet
    template_name = "tweets/tweets_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["like_list"] = Like.objects.filter(likeuser=self.request.user).values_list("likedtweet__pk", flat=True)
        return context


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    template_name = "tweets/tweets_delete.html"
    success_url = reverse_lazy("tweets:home")

    def test_func(self):
        tweet = self.get_object()
        return tweet.user == self.request.user


class LikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=self.kwargs["pk"])
        Like.objects.get_or_create(likeuser=request.user, likedtweet=tweet)
        context = {"likes_count": tweet.likedtweet.count()}
        return JsonResponse(context)


class UnlikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=self.kwargs["pk"])
        Like.objects.filter(likeuser=request.user, likedtweet=tweet).delete()
        context = {"likes_count": tweet.likedtweet.count()}
        return JsonResponse(context)


class GetLikesCountView(View):
    def get(self, request, tweet_id):
        tweet = get_object_or_404(Tweet, id=tweet_id)
        likes_count = tweet.likedtweet.count()
        return JsonResponse({"likes_count": likes_count})
