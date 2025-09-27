from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.conf import settings


class Politician(models.Model):
    name = models.CharField(max_length=255)
    party = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    biography = models.TextField(blank=True)
    social_links = models.JSONField(default=dict, blank=True,null=True)  # {"twitter": "..."}
    tags = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="politicians/")
    average_aura = models.FloatField(default=0.0)
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_average_aura(self):
        ratings = self.rating_set.all()
        if ratings.exists():
            self.average_aura = sum(r.aura_score for r in ratings) / ratings.count()
            self.save()

    def __str__(self):
        return f"{self.name} ({self.party})"


class Rating(models.Model):
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    aura_score = models.IntegerField(
        validators=[MinValueValidator(-999), MaxValueValidator(999)]
    )
    integrity = models.PositiveSmallIntegerField(default=0)
    effectiveness = models.PositiveSmallIntegerField(default=0)
    popularity = models.PositiveSmallIntegerField(default=0)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.politician.update_average_aura()



class Comment(models.Model):
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)