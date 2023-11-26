# Generated by Django 4.1.9 on 2023-11-26 07:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tweets", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Like",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "likedtweet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="likedtweet", to="tweets.tweet"
                    ),
                ),
                (
                    "likeuser",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="like",
            constraint=models.UniqueConstraint(fields=("likeuser", "likedtweet"), name="unique_like"),
        ),
    ]
