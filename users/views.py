from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic import CreateView, UpdateView, ListView
from posts.models import Post
from .forms import RegisterForm, UserProfileForm
from .models import UserProfile
from django.urls import reverse, reverse_lazy
import pyrebase
from django.contrib import messages
import os

firebaseConfig = {
    'apiKey':  os.environ.get('api_key'),
    'authDomain':  os.environ.get('authdomain'),
    "databaseURL":  os.environ.get('database'),
    'projectId': os.environ.get('project_id'),
    'storageBucket': os.environ.get('storagebucket'),
    'messagingSenderId': os.environ.get('sender_id'),
    'appId': os.environ.get('app_id'),
    'measurementId': os.environ.get('measurement_id')
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


@method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
@method_decorator(cache_page(60 * 1, cache="special_cache"), name='dispatch')
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


@method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
@method_decorator(cache_page(60 * 1, cache="special_cache"), name='dispatch')
class UserLoginView(LoginView):  # Initializing template for login view
    template_name = 'users/login.html'

    def form_valid(self, form):
        username = form['username'].value()  # getting the email from form object
        password = form['password'].value()  # getting the password from form object
        email = User.objects.filter(username=username).values('email')
        try:  # some basic validation of e-mail
            user = auth.sign_in_with_email_and_password(email[0]['email'], password)  # login with e-mail and password
            user_info = auth.get_account_info(user['idToken'])
            if user_info['users'][0]['emailVerified']:
                return super().form_valid(form)
            else:
                messages.error(self.request,
                               'Please verify your email')  # adding the errors in messages list which will be shown in message.html template
                return HttpResponseRedirect(reverse('users:login'))  # Redirecting to form page if there are any errors
        except:
            messages.error(self.request,
                           'Please check your password and e-mail')  # adding the errors in messages list which will be shown in message.html template
            return HttpResponseRedirect(reverse('users:login'))  # Redirecting to form page if there are any errors


@method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
@method_decorator(cache_page(60 * 1, cache="special_cache"), name='dispatch')
class UserLogoutView(LogoutView):
    template_name = 'users/login.html'


@method_decorator(login_required(login_url='/users/login'), name="dispatch")
@method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
@method_decorator(cache_page(60 * 1, cache="special_cache"), name='dispatch')
class UserProfileUpdateView(SuccessMessageMixin, UpdateView):
    model = UserProfile
    template_name = 'users/profile-update.html'
    form_class = UserProfileForm
    success_message = "Your Profile Has Been Updated!!!"
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(UserProfileUpdateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')

        return super(UserProfileUpdateView, self).get(request, *args, **kwargs)


@method_decorator(login_required(login_url='/users/login'), name="dispatch")
@method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
@method_decorator(cache_page(60 * 1, cache="special_cache"), name='dispatch')
class UserProfileView(ListView):
    template_name = 'users/my-profile.html'
    model = Post
    context_object_name = 'userposts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['userprofile'] = UserProfile.objects.get(user=self.request.user)
        return context

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-id')


@method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
@method_decorator(cache_page(60 * 1, cache="special_cache"), name='dispatch')
class UserPostView(ListView):
    template_name = 'users/user-post.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(user=self.kwargs['pk'])


@method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
@method_decorator(cache_page(60 * 1, cache="special_cache"), name='dispatch')
class UserListView(ListView):
    template_name = 'users/user-list.html'
    model = UserProfile
    context_object_name = 'profiles'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        return context
