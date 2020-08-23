from django import forms
from .models import Post, Comment, Image
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    category = forms.MultipleChoiceField(
        label='Categories', 
        widget=forms.CheckboxSelectMultiple, 
        choices=Post.CHOICES
    )

    class Meta:
        model = Post
        fields = ( 'title', 'category', 'text')

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image',]
##여러개의 이미지를 올리기 위해서 formset을 사용함/ 이미지 폼을 갖고와 엮어서 폼셋으로 만들어주는 역할을 함##
ImageFormSet = forms.inlineformset_factory(Post, Image, form=ImageForm, extra=10)
#inlineformset_factory(부모모델, 우리가 만드는 모델, 기본으로 들고오는 폼이미지 폼, 이미지의 개수)#
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username","email","password1","password2"]

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']