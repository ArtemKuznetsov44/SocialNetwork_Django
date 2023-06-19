from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core import validators
from datetime import date
import re

from main.models import *
from django.forms.widgets import *
from django.core.exceptions import ValidationError

patterns = {
    'email': r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', 
    'phone': r'\+7-9\d{2}-\d{3}-\d{2}-\d{2}', 
    'names': r'^[A-Z][a-z]{1,15}$'
}


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
        attrs={'class': "form-control", 'placeholder': '+7-9XX-XXX-XX-XX'}))

    gender = forms.ModelChoiceField(queryset=Gender.objects.all(
    ), empty_label='Gender', widget=Select(attrs={'class': 'form-select'}), required=True)

    date_of_birth = forms.DateField(label='Date of birht', required=True, widget=DateInput(
        attrs={'type': 'date', 'class': 'form-control',  'min': '1920-01-01',
               'max': date.today().strftime('%Y-%m-%d')}))

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

    def clean(self):
        cleaned_data = super().clean()

        min_date = date(1920, 1, 1)
        max_date = date.today()

        if not re.match(patterns['names'], cleaned_data.get('first_name')):
            # raise ValidationError(message="First Name is incorrect!")
            self.add_error('first_name', 'First Name is not valid.')
       
        if not re.match(patterns['names'], cleaned_data.get('last_name')):
            # raise ValidationError(message="Last Name is inccorrect!")
            self.add_error('last_name', 'Last Name is not valid.')
   
        
        if len(cleaned_data.get('username').strip()) < 8:
            # raise ValidationError(message='Username is inccorrect!')
            self.add_error('username', 'Username is not valid.')
     
        
        if not re.match(patterns['email'], cleaned_data.get('email')):
            # raise ValidationError(message='Email is inccorect!')
            self.add_error('email', 'E-mail is not valid.')
     

        if not re.match(patterns['phone'], cleaned_data.get('phone')): 
            # raise ValidationError(message='Phone number is inccorect! Should be: +7-9XX-XXX-XX-XX')
            self.add_error('phone', 'Phone number is not valid. Must be in format: +7-9XX-XXX-XX-XX')
     

        input_data = cleaned_data.get('date_of_birth')
        if input_data > max_date or input_data < min_date:
            # raise ValidationError(message='Data is inccorrect!')
            self.add_error('data_of_birth', 'Data is not valid.')
           

      
        

# This is the user authentication form (for log in operation):
class UserSignInForm(AuthenticationForm):
 
    username = forms.EmailField(label='E-mail', required=True,  widget=EmailInput(
        attrs={"class": "form-control", "placeholder": "email@gmail.com"}))
    # email = forms.EmailField(label='E-mail', required=True,  widget=EmailInput(
    #     attrs={"class": "form-control", "placeholder": "email@gmail.com"}))
    password = forms.CharField(label="Password", widget=PasswordInput(
        attrs={"class": "form-control", "placeholder": "Password"}))

    fields = ['email', 'password']

    def confirm_login_allowed(self, user):
        if not user:
            raise ValidationError('No such use in system.')

    def clean_username(self): 
        username = self.cleaned_data['username']
        if not re.match(patterns['email'], username): 
            raise ValidationError('Username is not valid.')
        
        return username

        
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

# This form is used in modal windows for updating user info:
class UpdateUserInfoForm(forms.ModelForm):

    first_name = forms.CharField(label='First Name', required=True, widget=TextInput(attrs={
        'class': 'form-control'
    }))

    last_name = forms.CharField(label='Last Name', required=True, widget=TextInput(attrs={
        'class': 'form-control'
    }))
    username = forms.CharField(label='Username', widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter new nickname...'}), required=True)

    gender = forms.ModelChoiceField(queryset=Gender.objects.all(),
                                    empty_label='Gender', widget=Select(attrs={'class': 'form-select'}), required=True)

    date_of_birth = forms.DateField(label='Date of birht', required=True, widget=DateInput(
        attrs={'type': 'date', 'class': 'form-control',  'min': '1920-01-01',
               'max': date.today().strftime('%Y-%m-%d')}))

    profile_img = forms.ImageField(label='Profile Image', required=False, widget=FileInput(attrs={
        'class': 'form-control'
    }))

    profile_back_img = forms.ImageField(label='Profile Background', required=False, widget=FileInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth',
                  'username', 'status', 'profile_img', 'profile_back_img']

        widgets = {
            'status': TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your status..."
            })
        }

    def clean(self):
        cleaned_data = super().clean()

        min_date = date(1920, 1, 1)
        max_date = date.today()

        if not re.match(patterns['names'], cleaned_data.get('first_name')):
            # raise ValidationError(message="First Name is incorrect!")
            self.add_error('first_name', 'First Name is not valid.')
           

        if not re.match(patterns['names'], cleaned_data.get('last_name')):
            # raise ValidationError(message="Last Name is inccorrect!")
            self.add_error('last_name', 'Last Name is not valid.')
           
        
        if len(cleaned_data.get('username').strip()) < 8:
            # raise ValidationError(message='Username is inccorrect!')
            self.add_error('username', 'Username is not valid.')
            
        
        input_data = cleaned_data.get('date_of_birth')
        if input_data > max_date or input_data < min_date:
            # raise ValidationError(message='Data is inccorrect!')
            self.add_error('data_of_birth', 'Data is not valid.')
            

