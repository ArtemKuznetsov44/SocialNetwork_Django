from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, View, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from main.forms import *
from main.models import *
from django.db.models import Q
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

    # This is the DetaileView class function where we can specify addition context for working template:
    def get_context_data(self, **kwargs):
        # This expression is used to get the already existing context on the page (so as not to lose it, but only add new data to it later):
        # SAVE ALREADY EXISTING CONTEXT ON THE PAGE:
        context = super().get_context_data(**kwargs)
        # Create new data for context list - a list of posts by current user:
        context["user_posts_objects"] = Post.objects.filter(
            user=self.object.id).order_by('created_at')

        # Create dictionary where key - post.id and value - count of likes:
        post_likes_count = {}
        post_comments_count = {}
        for post in context['user_posts_objects']:
            # For post by it id we get count of likes:
            post_likes_count[post.id] = PostLike.objects.filter(post=post.id).count()
            # For post by it id we get count of comments
            post_comments_count[post.id] = PostComment.objects.filter(post=post.id).count()
        
        context["post_likes_count"] = post_likes_count
        context["post_comments_count"] = post_comments_count
        context["user_photos_objects"] = UserPhoto.objects.filter(
            user=self.object.id).order_by('created_at')
        # Return new context which contains the ['user' and 'user_posts' and 'user_photos'] now:
        return context

class ShowGroups(ListView):
    model = Group
    paginate_by = 100
    template_name="main/groups.html"
    context_object_name = "groups"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    # def get(self, request):
    #     user = self.request.user
    #     if user and user.is_authenticated:
    #         return render(request, template_name='groups')

    #     return redirect('start_page')


class ShowGroup(DetailView):
    model = Group
    template_name = "main/group.html"
    context_object_name = "group"

    # This is the DetaileView class function where we can specify addition context for working template:
    def get_context_data(self, **kwargs):
        # This expression is used to get the already existing context on the page (so as not to lose it, but only add new data to it later):
        # SAVE ALREADY EXISTING CONTEXT ON THE PAGE:
        context = super().get_context_data(**kwargs)
        # Create new data for context list - a list of posts by current user:
        context["group_posts_objects"] = Post.objects.filter(
            group=self.object.id).order_by('created_at')

        # Create dictionary where key - post.id and value - count of likes:
        post_likes_count = {}
        post_comments_count = {}
        for post in context['group_posts_objects']:
            # For post by it id we get count of likes:
            post_likes_count[post.id] = PostLike.objects.filter(post=post.id).count()
            # For post by it id we get count of comments
            post_comments_count[post.id] = PostComment.objects.filter(post=post.id).count()
        
        context["post_likes_count"] = post_likes_count
        context["post_comments_count"] = post_comments_count
        context["user_photos_objects"] = UserPhoto.objects.filter(
            group=self.object.id).order_by('created_at')
        # Return new context which contains the ['user' and 'user_posts' and 'user_photos'] now:
        return context

class ShowPhotosPage(ListView):
    pass

# This class based view is used for ajax post additing:
class CreateGroupAjax(View): 
    def post(self, request): 
        group_name = request.POST.get('group_name')
        group_info = request.POST.get('group_info')
        group_img = request.FILES.get('group_img')

        group_theme = request.POST.get('group_theme')
        theme = GroupTheme.objects.get(id = group_theme)

        group = Group.objects.create(
            admin = self.request.user,
            group_name = group_name,
            group_info = group_info,
            group_theme = theme,
            group_img = None,
            )
        group.group_img = group_img

        group.save()

        if group: 
            return JsonResponse(
                data={'ok': 'Success!'}, 
                status=201
            )

        return JsonResponse(
            data={'error': 'Error in post creation'},
            status=400
        )

# This class based view is used for ajax photo additing:
class AddNewPhotoAjax(View):
   # This method is used when we send post requests to the url 'profile'
      def post(self, request):
        # Get photo from files:
        upload_photo = request.FILES.get('photo')
        # Checking it:
        if upload_photo:
            # Try to create new modal instance like new record in UserPhoto model:
            created = UserPhoto.objects.create(
                user=self.request.user, photo=upload_photo)
            # Checking it:
            if created:                
                return JsonResponse(data={'ok': 'Success!'}, status=201)
            return JsonResponse(
                data={'error': 'Faild to upload current image'},
                status=400
            )
        return JsonResponse(
            data={'error': 'Image was not found in request'},
            status=400
        )


# This class based view is used for ajax post additing:
class AddNewPostAjax(View): 
    def post(self, request): 
        text = request.POST.get('text')
        like_status = request.POST.get('like_status')
        comment_status = request.POST.get('comment_status')
        content = request.FILES.get('content')

        # If we do not get text and content:
        if not text and not content:
            return JsonResponse(
                data={'error': 'The post must contain at least text or a content file'}, 
                status=400
            )
        
        # If we get content but content type is not available:
        if content and not get_content_type(content._name):
            return JsonResponse(
                data={'error': 'This file extension is not supported'}, 
                status=400
            )
        
        # In oposite case crete new Post object:
        # Create new instance for geting id:
        new_post = Post.objects.create(
            user=self.request.user,
            group=None, 
            # Checkin text:
            text=(text if text else None), 
            content=None, 
            content_type=None,
            like_status= (True if like_status == 'on' else False),
            comment_status=(True if comment_status == 'on' else False))

        # Update content field if content exists:
        new_post.content = (content if content else None)
        
        # Saving:
        new_post.save()
        
        if new_post: 
            return JsonResponse(
                data={'ok': 'Success!'}, 
                status=201
            )
        
        return JsonResponse(
            data={'error': 'Error in post creation'},
            status=400
        )

# This class based view is used for add comments to the post:
class AddNewCommentAjax(View): 

    def post(self, request): 

        if self.request.POST.get('text') == 'get_comments' and self.request.POST.get('post_id'):
            post_id = int(self.request.POST.get('post_id'))
            comments = PostComment.objects.filter(post=post_id)
            
            if not comments:
                return JsonResponse(data={'error': 'Now comments yet! You can be the first one!', 'post_id': post_id}, status=400 ) 

            serialized_comments = [{'first_name': comment.user.first_name, 'last_name': comment.user.last_name, 'comment': comment.comment } for comment in comments]
            return JsonResponse(data={'comments': serialized_comments, 'post_id': post_id}, status=201)
        
        if self.request.POST.get('text') == 'leave_comment' and self.request.POST.get('post_id'):
            post_id = int(self.request.POST.get('post_id'))
            comment = self.request.POST.get('data')

            comment = PostComment.objects.create(user=self.request.user, post=Post.objects.get(pk=post_id), comment=comment)

            if comment: 
                return JsonResponse(data={'ok': 'Success!'}, status=201)
            
            return JsonResponse(data={'error': 'Error in comment creation'}, status=400)


class AddLikeAjax(View): 
    def post(self, request): 

        post_id = int(self.request.POST.get('post_id'))

        post_like = PostLike.objects.filter(Q(user=self.request.user.pk) & Q(post=post_id))

        if not post_like: 
            post_like = PostLike.objects.create(user=self.request.user, post=Post.objects.get(pk=post_id))
            if post_like: 
                return JsonResponse(data={'create': True}, status=201)

        post_like.delete() 
        return JsonResponse(data={'create': False}, status=201)


class DeletePostAjax(View):
    def post(self, request):
        post_id = int(self.request.POST.get('post_id'))
        post_object = Post.objects.get(pk=post_id)

        if post_object:
            if post_object.user == self.request.user:
                post_object.delete()
                return JsonResponse(data={'ok': 'Post was deleted'}, status=201)
            else:
                return JsonResponse(data={'error': 'You dont have permission for this action!'}, status=400)
   