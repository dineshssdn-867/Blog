from functools import lru_cache

import pyrebase
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView

from posts.models import Post
from .forms import RegisterForm, UserProfileForm
from .models import UserProfile

firebaseConfig = {
    'apiKey': "AIzaSyAGJFENEV_gia2sI-9lZnm25Va9Z8JASIU",
    'authDomain': "d-s-blog-7c796.firebaseapp.com",
    "databaseURL": "https://d-s-blog-7c796-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'projectId': "d-s-blog-7c796",
    'storageBucket': "d-s-blog-7c796.appspot.com",
    'messagingSenderId': "747551234600",
    'appId': "1:747551234600:web:654f9d2994eb7c7445b31d",
    'measurementId': "G-QRD0E9BPB3"
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_message = "Please click the update button to update the profile to give the best public view about yourself"
    success_url = reverse_lazy('users:myprofile')

    def form_valid(self, form):
        email = form['email'].value()
        password = form['password1'].value()
        try:
            user = auth.create_user_with_email_and_password(email, password)
            login = auth.sign_in_with_email_and_password(email, password)
            auth.send_email_verification(login['idToken'])
            return super().form_valid(form)
        except:
            messages.error(self.request, 'E-mail is already taken please enter a new e-mail')
            return HttpResponseRedirect(reverse('users:register'))


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    template_name = 'users/login.html'


@method_decorator(login_required(login_url='/users/login'), name="dispatch")
class UserProfileUpdateView(SuccessMessageMixin, UpdateView):
    model = UserProfile
    template_name = 'users/profile-update.html'
    form_class = UserProfileForm
    success_message = "Your Profile Has Been Updated!!!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)
        self.object.save()
        return super(UserProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('users:update_profile', kwargs={'slug': self.object.slug})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(UserProfileUpdateView, self).get(request, *args, **kwargs)


@method_decorator(login_required(login_url='/users/login'), name="dispatch")
class UserProfileView(ListView):
    template_name = 'users/my-profile.html'
    model = UserProfile
    context_object_name = 'userposts'
    paginate_by = 5

    @lru_cache(maxsize=None)
    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        print(self.request.user)
        context['userprofile'] = UserProfile.objects.get(user=self.request.user)
        return context

    @lru_cache(maxsize=None)
    def get_queryset(self):
        return Post.objects.using('posts').filter(user=self.request.user).order_by('-id')


class UserPostView(ListView):
    template_name = 'users/user-post.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 5

    @lru_cache(maxsize=None)
    def get_queryset(self):
        return Post.objects.using('posts').filter(user=self.kwargs['pk'])


class UserListView(ListView):
    template_name = 'users/user-list.html'
    model = UserProfile
    context_object_name = 'profiles'
    paginate_by = 5

    @lru_cache(maxsize=None)
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        return context
