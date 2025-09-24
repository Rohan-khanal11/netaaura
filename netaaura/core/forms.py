from django import forms
from .models import Politician, Rating, Comment

class PoliticianForm(forms.ModelForm):
    class Meta:
        model = Politician
        fields = ["name", "party", "position", "biography", "social_links", "tags", "image"]
        widgets = {
            "biography": forms.Textarea(attrs={"rows": 4}),
            "social_links": forms.Textarea(attrs={"rows": 2, "placeholder": '{"twitter": "https://..."}'}),
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["aura_score", "integrity", "effectiveness", "popularity", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 2, "placeholder": "Write your comment..."}),
        }
