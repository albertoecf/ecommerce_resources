from django import forms
from .models import ReviewRatingClass

class ReviewFormClass(forms.ModelForm):
    class Meta:
        model = ReviewRatingClass
        fields = ['subject','review','rating']
