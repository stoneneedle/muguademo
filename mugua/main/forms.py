from django import forms

class CreateCourse(forms.Form):
    title = forms.CharField(label="Title", max_length=120)

class CreateDiscussionPost(forms.Form):
    title = forms.CharField(label="Title", max_length=120)
    message = forms.CharField(widget=forms.Textarea)

class CreateDiscussionPostReply(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField(required=False)