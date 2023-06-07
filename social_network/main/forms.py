from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


from main.models import *
from django.forms.widgets import *


# From for user registration which extends from default UserCreationForm from django:
class UserRegistrationForm(UserCreationForm):
    # Fields specification:
    first_name = forms.CharField(label='First Name', required=True, widget=TextInput(
        attrs={"class": "form-control", "placeholder": "First name"}))
    last_name = forms.CharField(label='Last Name', required=True, widget=TextInput(
        attrs={"class": "form-control", "placeholder": "Middle name"}))
    username = forms.CharField(label='username', widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nickname'}), required=True)
    email = forms.EmailField(label='E-mail', required=True,  widget=EmailInput(
        attrs={"class": "form-control", "placeholder": "email@gmail.com"}))
    phone = forms.CharField(label='Phone', required=True, widget=TextInput(
        attrs={'class': "form-control", 'placeholder': 'Phone number'}))

    gender = forms.ModelChoiceField(queryset=Gender.objects.all(
    ), empty_label='Gender', widget=Select(attrs={'class': 'form-select'}), required=True)

    date_of_birth = forms.DateField(label='Date of birht', required=True, widget=DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    password1 = forms.CharField(label="password", widget=PasswordInput(
        attrs={"class": "form-control", "placeholder": "Password"}), required=True)
    password2 = forms.CharField(label="password confirm", widget=PasswordInput(
        attrs={"class": "form-control", "placeholder": "Confirm password"}), required=True)

    # Meta-info for form class:
    class Meta:
        # Model for work:
        model = User
        # Filed for usage (order in view would be the same if we use such sintaxe [] )
        fields = ['first_name', 'last_name', 'username', 'email',
                  'phone', 'gender', 'date_of_birth', 'password1', 'password2']

# This is the user authentication form (for log in operation):
class UserSignInForm(AuthenticationForm):
    # This method is the initialization method where we delte from form username field: 
    # Fields specification (we will use only 2 fields: email and password):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields.pop('username')

    username = forms.EmailField(label='E-mail', required=True,  widget=EmailInput(
        attrs={"class": "form-control", "placeholder": "email@gmail.com"}))
    # email = forms.EmailField(label='E-mail', required=True,  widget=EmailInput(
    #     attrs={"class": "form-control", "placeholder": "email@gmail.com"}))
    password = forms.CharField(label="password", widget=PasswordInput(
        attrs={"class": "form-control", "placeholder": "Password"}))
    
    fields = ['email', 'password']


# This is the form for additing new photos by user:
class AddPhotosForm(forms.ModelForm): 
    class Meta: 
        model = UserPhoto
        fields = ['photo'] 

        widgets = {
            'photo': FileInput(attrs={
                'class': 'form-control'
            })
        }

# This is the form for additing new posts by user:
class AddPostsForm(forms.ModelForm): 
    class Meta: 
        model = Post
        fields = ['text', 'content', 'like_status', 'comment_status']

        widgets = {
            'text': Textarea(attrs={
                "class": "form-control", 
                "rows": "5",
                "placeholder": "Some content here..."
            }), 
            'content': FileInput(attrs={
                'class': 'form-control'
            }), 
            'like_status': CheckboxInput(attrs={
                'class': 'form-check-input'
            }), 
            'comment_status': CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

# This is the form for additing new comments by user:
class AddCommentForm(forms.ModelForm): 
    class Meta: 
        model = PostComment
        fields = ['comment']

        widgets = {
            'comment': Textarea(attrs={
                'class': 'form-control', 
                'rows': '3', 
                'placeholder': 'Leave your comment here...'
            })
        }