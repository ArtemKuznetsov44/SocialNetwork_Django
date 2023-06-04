from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from main.forms import *
from main.models import *
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect

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

# This is the simple View base class for rendering our start_page:


class ShowStartPage(View):
    # For get method (when we go to this page):
    def get(self, request):
        # Try to get user from request:
        user = self.request.user
        # If user not none and user is authenticated:
        if user and user.is_authenticated:
            # Redirect hime to the profile page with param pk where pk is the current user primary key:
            return redirect('profile', pk=user.pk)

        # In other case just render the base start page with opportunites for signIn or registration:
        return render(request, template_name='main/start_page.html')


# This it the class based view for authenticate users:
class UserSignIn(LoginView):
    # Specify the form class:
    form_class = UserSignInForm
    # Specify the template for working for:
    template_name = 'main/sign_in.html'

    # If form is valid and we get success:
    def get_success_url(self):
        # Geting user from request:
        user = self.request.user
        # Making the success_url from profile page with the pk from current user:
        return reverse_lazy('profile', kwargs={"pk": user.pk})


# This is the class based view for loging out for user:
class UserSignOut(LogoutView):
    def get_success_url(self):
        return reverse_lazy('start_page')


# This is the class based view for show profile of current user
class ShowProfile(DetailView):
    model = User
    template_name = "main/profile.html"
    context_object_name = "user"

    # def post(self, request, pk):
    #     upload_photo = request.FILES.get('photo')
    #     if upload_photo:
    #         created = UserPhoto.objects.create(user=self.request.user, photo=upload_photo)
    #         if created:
    #             return JsonResponse(data={'success':'Hello'}, status=201)
    #         return JsonResponse (
    #             data={'error': 'Faild to upload current image'},
    #             status=400
    #         )
    #     return JsonResponse (
    #         data={'error': 'Image was not found in request'},
    #         status=400
    #     )

    # This is the DetaileView class function where we can specify addition context for working template:
    def get_context_data(self, **kwargs):
        # This expression is used to get the already existing context on the page (so as not to lose it, but only add new data to it later):
        # SAVE ALREADY EXISTING CONTEXT ON THE PAGE:
        context = super().get_context_data(**kwargs)
        # Create new data for context list - a list of posts by current user:
        context["user_posts_objects"] = Post.objects.filter(
            user=self.request.user.pk)
        context["user_photos_objects"] = UserPhoto.objects.filter(
            user=self.request.user.pk)
        # Return new context which contains the ['user' and 'user_posts' and 'user_photos'] now:
        return context

# This class based view is used for ajax photo additing:


# ВОТ ТУТ: 
class AddNewPhotoAjax(View):

    def post(self, request):
        upload_photo = request.FILES.get('photo')
        if upload_photo:
            created = UserPhoto.objects.create(
                user=self.request.user, photo=upload_photo)
            if created:
                return JsonResponse(data={'success': 'Hello'}, status=201)
            return JsonResponse(
                data={'error': 'Faild to upload current image'},
                status=400
            )
        return JsonResponse(
            data={'error': 'Image was not found in request'},
            status=400
        )
