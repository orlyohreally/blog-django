from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import (authenticate, get_user_model, login, logout)
from django.contrib.auth.models import User
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "tag_list", "image"]
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
User = get_user_model()
class UserSigninForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username = username, password = password)
            if not user:
                raise forms.ValidationError("This user does not exist.")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password.")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)