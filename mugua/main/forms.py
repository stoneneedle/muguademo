from django import forms

class CreateAssignment(forms.Form):
    title = forms.CharField(label="Title", max_length=120)
    max_grade_pts = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea)

class CreateCourse(forms.Form):
    title = forms.CharField(label="Title", max_length=120)

class CreateDiscussionPost(forms.Form):
    title = forms.CharField(label="Title", max_length=120)
    message = forms.CharField(widget=forms.Textarea)

class CreateDiscussionPostReply(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

class CreateModule(forms.Form):
    title = forms.CharField(label="Title", max_length=120)
    #course = forms.CharField(label="Course", max_length=120)

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField(required=False)