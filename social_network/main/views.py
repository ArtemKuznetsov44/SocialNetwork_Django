from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, View, ListView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from main.forms import *
from main.models import *
from django.db.models import Q
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from datetime import datetime


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
            return redirect('profile', slug=user.slug)

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
        return reverse_lazy('profile', kwargs={"slug": user.slug})


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
            post_likes_count[post.id] = PostLike.objects.filter(
                post=post.id).count()
            # For post by it id we get count of comments
            post_comments_count[post.id] = PostComment.objects.filter(
                post=post.id).count()

        context["post_likes_count"] = post_likes_count
        context["post_comments_count"] = post_comments_count
        context["user_photos_objects"] = UserPhoto.objects.filter(
            user=self.object.id).order_by('created_at')
        # Return new context which contains the ['user' and 'user_posts' and 'user_photos'] now:
        return context

# This class based view is used for edit profile in modal window with ajax:


class ProfileEditingAjax(View):
    def get(self, request):
        user = User.objects.get(pk=self.request.user.pk)
        if user:
            return JsonResponse(data={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'gender': user.gender.pk,
                'date_of_birth': user.date_of_birth,
                'username': user.username,
                'status': user.status,
            }, status=200)
        return JsonResponse(data={'error': 'Error in finding such user'}, status=404)

    def post(self, request):
        user = User.objects.get(pk=self.request.user.pk)
        if user:
            entered_username = self.request.POST.get('username')

            if (entered_username and entered_username != self.request.user.username and User.objects.filter(username=entered_username)):
                return JsonResponse(data={'error': 'Shuch username is already used!'}, status=403)

            user.first_name = self.request.POST.get('first_name')
            user.last_name = self.request.POST.get('last_name')
            user.gender = Gender.objects.get(
                pk=self.request.POST.get('gender'))
            user.date_of_birth = self.request.POST.get('date_of_birth')
            user.username = self.request.POST.get('username')
            user.status = self.request.POST.get('status')
            user.profile_img = self.request.FILES.get(
                'profile_img') if self.request.FILES.get('profile_img') else user.profile_img
            user.profile_back_img = self.request.FILES.get(
                'profile_back_img') if self.request.FILES.get('profile_back_img') else user.profile_back_img
            user.save()
            return JsonResponse(data={'ok': 'Success!'}, status=200)

        return JsonResponse(data={'error': 'Error in finding such user'}, status=404)


class ShowMessengerPage(ListView):
    model = Chat
    template_name = 'main/messenger.html'
    context_object_name = 'chats'


    def get_queryset(self):
        # Receive QuerySet of Chats for current user:
        return Chat.objects.filter(chatmember__user=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all().exclude(
                pk=self.request.user.pk).exclude(is_staff=True).order_by('first_name')
        

        opponents = []

        for chat in self.object_list: 
            # Получаем участников чата:
            members = ChatMember.objects.filter(chat=chat.id)
            for member in members:
                if member.user != self.request.user:
                    opponents.append(member.user)


        context['opponents'] = opponents
        return context



class ShowDialogPage(DetailView):
    model = Chat
    template_name = 'main/dialog.html'
    context_object_name = 'dialog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dialog_name = ChatMember.objects.filter(Q(chat=self.object.pk) & ~Q(user=self.request.user.pk)).first()
        context['dialog_name'] = dialog_name.user.first_name + " " + dialog_name.user.last_name
        context["messages"] = Message.objects.filter(chat=self.object.pk).all().order_by('sent_at') 
        return context
    


# This is the class based view for show friends of current user:
class ShowFriendsPage(ListView):
    model = User                        # Specify the model.
    template_name = 'main/friends.html'  # Specify the template.
    # Specify the name of our main query_set (we get it in get_queryset method).
    context_object_name = 'friends'

    def get_queryset(self):
        current_user = self.request.user

        # Get friend requeists where we are sender or receiver user:
        friend_requests = FriendRequest.objects.filter(Q(is_accepted=True) & (
            Q(sender=self.request.user.pk) | Q(to_user=self.request.user.pk)))

        # Create the lists for ids (we need to get only users from friend_requests without us):
        my_friends_ids = []

        # In loop we compare that request sender is current user, so we get request.to_user.id
        # and if request.to_user is the current_user - we get request.sender.id.
        # my_friends_ids is the list which contains only ids of our friends, because we look only accepted requests.
        for request in friend_requests:
            if request.sender == current_user:
                my_friends_ids.append(request.to_user.id)
            elif request.to_user == current_user:
                my_friends_ids.append(request.sender.id)

        # Return the QuerySet like object from User model where user's ids in my_friends_ids:
        return User.objects.filter(id__in=my_friends_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get only not staff and not current user from request (for users chapter in template):
        context["users"] = User.objects.all().exclude(
            pk=self.request.user.pk).exclude(is_staff=True).order_by('first_name')

        # Friend request objects which was sent by us:
        friend_requests_sent = FriendRequest.objects.filter(
            sender=self.request.user.pk, is_accepted=False)

        # Getting user's ids which are receiving requests from us:
        receiving_user = []
        for friend_req in friend_requests_sent:
            receiving_user.append(friend_req.to_user)

        # Users who receive the request from us.
        context['receiving_user'] = receiving_user

        user_followers = UserFollower.objects.filter(user=self.request.user.pk)

        followers = []
        for user_follower in user_followers:
            followers.append(user_follower.follower)

        context['followers'] = followers

        # Friend requests which we receive (for My Requests chapter in template)
        context["friend_requests_received"] = FriendRequest.objects.filter(
            to_user=self.request.user.pk, is_accepted=False)

        return context


class ShowOnePost(DetailView): 
    model = Post
    template_name = 'main/one_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     

        post_likes_count = PostLike.objects.filter(post=self.object.pk).count()
        post_comments_count = PostComment.objects.filter(post=self.object.pk).count()
           
        context["post_likes_count"] = post_likes_count
        context["post_comments_count"] = post_comments_count

        return context
    


class ShowPhotosPage(View): 
    pass


class MessageAjax(View):
    def post(self, request):
        sender_id = int(self.request.POST.get('sender_id'))
        message = self.request.POST.get('message')
        chat_id = int(self.request.POST.get('chat'))
        if sender_id and message and chat_id:
            new_message = Message.objects.create(text=message, sender=User.objects.get(
                pk=sender_id), content_type=ContentType.objects.get(name='text'), chat=Chat.objects.get(pk=chat_id))
            
            if new_message: 
                return JsonResponse(data={'ok': 'Message was succesfuly created!'}, status=201)
            
            return JsonResponse(data={'error': 'Error in new_message creation proccess!'}, status=400)
        
        return JsonResponse(data={'error': 'sender_id, message or chat_id are specified incorrectly!'}, status=400)
    
    def get(self, request):
        last_msg_id = self.request.GET.get('last_msg_id')
        last_msg_id = None if last_msg_id == '' else int(last_msg_id)

        chat_id = int(self.request.GET.get('chat_id')) 
        if not last_msg_id and not chat_id:
            return JsonResponse(data={'error': 'No params were given!'}, status=404)

        if not last_msg_id and chat_id: 
            message = Message.objects.filter(chat=chat_id).order_by('sent_at').last()
        else: 
            message = Message.objects.filter(chat=chat_id, pk__gt=last_msg_id).first()
        
        if message: 
            serialized_message = {
                'pk' : message.pk, 
                'sender_first_name': message.sender.first_name, 
                'sender_last_name': message.sender.last_name,
                'text': message.text, 
                'sent_at': message.sent_at.strftime("%B %d, %Y, %I:%M %p")
            }
            return JsonResponse(data={'ok': serialized_message}, status=200)
        
        return JsonResponse(data={'ok': ""}, status=200)
     


class StartDialogAjax(View):
    def post(self, request):
        user_id = int(self.request.POST.get('user_id'))
        if user_id:
            current_chat = Chat.objects.filter(
                chatmember__user=self.request.user.pk).filter(chatmember__user=user_id).first()

            if not current_chat:
                new_chat = Chat.objects.create(is_private=True)
                new_chat_member_one = ChatMember.objects.create(
                    user=self.request.user, chat=new_chat)
                new_chat_member_second = ChatMember.objects.create(
                    user=User.objects.get(pk=user_id), chat=new_chat)

                if new_chat and new_chat_member_one and new_chat_member_second:
                    return JsonResponse(data={'ok': new_chat.pk}, status=201)

                return JsonResponse(data={'error': 'Error in creation proccess!'}, status=400)
            else:
                return JsonResponse(data={'ok': current_chat.pk}, status=200)

        return JsonResponse(data={'error': 'Error in getin user_id!'}, status=400)


class RequestAjax(View):
    def post(self, request):
        task = self.request.POST.get('task')
        if task == 'send':
            to_user_id = int(self.request.POST.get('user_id'))
            if to_user_id and not FriendRequest.objects.filter(sender=self.request.user.pk, to_user=to_user_id):
                new_request = FriendRequest.objects.create(
                    sender=self.request.user, to_user=User.objects.get(pk=to_user_id))
                if new_request:
                    return JsonResponse(data={'ok': 'Success!'}, status=201)
                return JsonResponse(data={'error': 'Error in request creation process'}, status=400)

            return JsonResponse(data={'error': 'Such request is already exists or to_user_id incorrect!'}, status=403)
        elif task == 'accept':
            sender_id = int(self.request.POST.get('user_id'))
            if sender_id:
                friend_request = FriendRequest.objects.get(
                    Q(sender=sender_id) & Q(to_user=self.request.user.pk))

                if not friend_request:
                    return JsonResponse(data={'error': 'Error in finding current request'}, status=400)

                friend_request.is_accepted = True
                friend_request.save()
                return JsonResponse(data={'ok': 'We become friends!'}, status=201)

            return JsonResponse(data={'error': 'You are already friend or sender_id is incorrect!'}, status=403)
        elif task == 'make-follower':
            follower_id = int(self.request.POST.get('user_id'))
            if follower_id and not UserFollower.objects.filter(user=self.request.user.pk, follower=follower_id):
                new_follower = UserFollower.objects.create(
                    user=self.request.user, follower=User.objects.get(pk=follower_id))
                if new_follower:
                    return JsonResponse(data={'ok': 'Success!'}, status=201)

                return JsonResponse(data={'error': 'Error in new_follower creation poccess!'}, status=400)

            return JsonResponse(data={'error': 'Such follower is already exist our follower_id is incorrect!'}, status=403)


class DeleteFriendAjax(View): 

    def get(self, request): 
        task = self.request.GET.get('task')
        if task == 'delete-friend':
            friend_id =  self.request.GET.get('user_id') 
            if friend_id and len(friend_id.strip()) > 0:
                friend_id = int(friend_id)

                friend = FriendRequest.objects.filter(is_accepted=True, sender=self.request.user.pk, to_user=friend_id)

                if not friend: 
                    friend = FriendRequest.objects.filter(is_accepted=True, sender=friend_id, to_user=self.request.user.pk)
                
                if not friend: 
                    return JsonResponse(data={'error': 'No such friend!'}, status=404)

                friend.delete()

                return JsonResponse(data={'ok': 'Success!'}, status=200)
            
            return JsonResponse(data={'error': 'No params were give (friend_id)'}, status=400)

        elif task == 'delete-follower':
            follower_id = self.request.GET.get('user_id')

            if follower_id and len(follower_id.strip()) > 0: 
                follower_id = int(follower_id)

                follower = UserFollower.objects.filter(user=self.request.user.pk, follower=follower_id)

                if not follower: 
                    return JsonResponse(data={'error': 'No such follower!'}, status=404)
                
                follower.delete()
                
                return JsonResponse(data={'ok', 'Success!'}, status=200)

            return JsonResponse(data={'error': 'Invalid param or param is not exists!'}, status=400)



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
            like_status=(True if like_status == 'on' else False),
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
                return JsonResponse(data={'error': 'Now comments yet! You can be the first one!', 'post_id': post_id}, status=400)

            serialized_comments = [{'first_name': comment.user.first_name,
                                    'last_name': comment.user.last_name, 'comment': comment.comment} for comment in comments]
            return JsonResponse(data={'comments': serialized_comments, 'post_id': post_id}, status=201)

        if self.request.POST.get('text') == 'leave_comment' and self.request.POST.get('post_id'):
            post_id = int(self.request.POST.get('post_id'))
            comment = self.request.POST.get('data')

            comment = PostComment.objects.create(
                user=self.request.user, post=Post.objects.get(pk=post_id), comment=comment)

            if comment:
                return JsonResponse(data={'ok': 'Success!'}, status=201)

            return JsonResponse(data={'error': 'Error in comment creation'}, status=400)


class AddLikeAjax(View):
    def post(self, request):
        post_id = int(self.request.POST.get('post_id'))
        post_like = PostLike.objects.filter(
            Q(user=self.request.user.pk) & Q(post=post_id))

        if not post_like:
            post_like = PostLike.objects.create(
                user=self.request.user, post=Post.objects.get(pk=post_id))
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

class DeletePhotoAjax(View):
    def post(self, request): 
        photo_id = int(self.request.POST.get('photo_id'))
        photo_object = UserPhoto.objects.get(pk=photo_id)

        if photo_object: 
            if photo_object.user == self.request.user: 
                photo_object.delete()
                return JsonResponse(data={'ok': 'Photo was deleted'}, status=201)
            else:
                return JsonResponse(data={'error': 'You dont have permission for this action!'}, status=400)