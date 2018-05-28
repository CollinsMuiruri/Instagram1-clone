from django import forms
from .models import Image, Comment, Profile


class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name', max_length=30)
    email = forms.EmailField(label='Email')


class InfoImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['editor', 'pub_date']
        widgets = {'tags': forms.CheckboxSelectMultiple()}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user', 'comment_date', 'image']


class UploadForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['user', 'likes', 'upload_date', 'profile']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
