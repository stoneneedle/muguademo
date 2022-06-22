from django import forms

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField(required=False)

class CreateDiscussionPost(forms.Form):
    title = forms.CharField(label="Title", max_length=120)
    message = forms.CharField(widget=forms.Textarea)
