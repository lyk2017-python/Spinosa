from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField()
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))