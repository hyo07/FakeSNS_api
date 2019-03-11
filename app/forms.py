from django import forms
from .models import Article, Profile


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(attrs={'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "introduction", "sex",
        )
