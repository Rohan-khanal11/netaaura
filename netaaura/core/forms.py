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
        fields = ['aura_score']
        widgets = {
            'aura_score': forms.NumberInput(attrs={'type': 'range', 'min': -999, 'max': 999})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "placeholder": "Write your comment..."})
        }
