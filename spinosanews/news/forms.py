from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField()
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))
from news.models import *

class CreateNewsForm (forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateNewsForm,self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['rows'] = 3

    class Meta:
        model = News
        exclude = [
            "id",
            "likes",
            "reports",
            "status",
            "slug",
            "publish_date",
        ]

