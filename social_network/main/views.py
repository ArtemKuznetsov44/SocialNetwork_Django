from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, CreateView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from main.forms import *
from main.models import * 
from django.urls import reverse_lazy



# Create your views here.
class UserProfile(DetailView):
    model = User
    template_name = "main/profile.html"
    context_object_name = "user"


# This is a class-based view - CreateView - 
# View for creating a new object, with a response rendered by a template.
class UserRegister(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "main/registration.html"
    
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return reverse_lazy('sign_in')

# class UserSingIn(View): 
#     template_name = "main/sign_in.html"

#     def get(self, request): 
#         context = {
#             'form' : UserSignInForm()
#         }
#         return render(request, self.template_name, context)

#     def post(self, request): 
#         form = UserSignInForm(request.POST)

#         if form.is_valid(): 
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(email=email, password=password)
#             if user: 
#                 login(request, user)
#                 return reverse_lazy('start_page')
        
#         context = {'form': form}

#         return render(request, self.template_name, context)

def show_start_page(request): 
    return render(request, template_name='main/start_page.html')

class UserSignIn(LoginView): 
    form_class = UserSignInForm
    template_name = 'main/sign_in.html'

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('profile', kwargs={"pk": user.pk})


class ShowProfile(DetailView): 
    model = User
    template_name = "main/profile.html" 
    context_object_name = "user"
