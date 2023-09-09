# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView
from django.views.generic.list import ListView

from .models import Tweet


class HomeView(LoginRequiredMixin, ListView):
    template_name = "tweets/home.html"
    model = Tweet
    context_object_name = "tweets"
    queryset = model.objects.select_related("user")


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


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "tweets/tweets_delete.html"
    model = Tweet
    success_url = reverse_lazy("tweets:home")
