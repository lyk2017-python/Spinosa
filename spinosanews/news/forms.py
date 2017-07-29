from django import forms
from news.models import *

class CreateNewsForm (forms.ModelForm):
    class Meta:
        model = News
        exclude = [
            "id",
            "likes",
            "reports",
            "status",
            "slug",
        ]

