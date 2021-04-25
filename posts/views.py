from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F, Q
from django.http import HttpResponseRedirect, request
from django.shortcuts import get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from myarchive.models import Archive
from users.models import UserProfile
from .forms import PostCreationForm, PostUpdateForm, CreateCommentForm
from .models import Post, Category, Tag
from functools import lru_cache


class IndexView(ListView):
    template_name = "posts/index.html"
    model = Post
    context_object_name = 'posts'
    paginate_by = 3

    @lru_cache(maxsize=None)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['slider_posts'] = Post.objects.using('posts').all().filter(slider_post=True).order_by('id')
        return context


@method_decorator(login_required(login_url='users/login'), name="dispatch")
class MyView(ListView):
    template_name = "posts/index.html"
    model = Post
    paginate_by = 3

    @lru_cache(maxsize=None)
    def get_queryset(self):
        self.category = UserProfile.objects.using('users').filter(user=self.request.user).values('category_like')
        return super().get_queryset()

    @lru_cache(maxsize=None)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyView, self).get_context_data(**kwargs)
        for category in self.category:
            category = category['category_like']
        context['slider_posts'] = Post.objects.using('posts').filter(slider_post=True).filter(category=category).order_by('-pk')
        context['posts'] = Post.objects.using('posts').filter(category=category).order_by('-pk')
        return context


class PostDetail(DetailView, FormMixin):
    template_name = 'posts/detail.html'
    model = Post
    context_object_name = 'single'
    form_class = CreateCommentForm

    @lru_cache(maxsize=None)
    def get(self, request, *args, **kwargs):
        self.hit = Post.objects.using('posts').filter(id=self.kwargs['pk']).update(hit=F('hit') + 1)
        return super(PostDetail, self).get(request, *args, **kwargs)

    @lru_cache(maxsize=None)
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['previous'] = Post.objects.using('posts').filter(id__lt=self.kwargs['pk']).order_by('-pk').first()
        context['next'] = Post.objects.using('posts').filter(id__gt=self.kwargs['pk']).order_by('pk').first()
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        context['total_likes'] = stuff.total_likes()
        liked = False
        if stuff.likes.using('users').filter(id=self.request.user.id).exists():
            liked = True
        context['form'] = self.get_form()
        context['liked']= liked
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.instance.post = self.object
            form.save()
            return super(PostDetail, self).form_valid(form)
        else:
            return super(PostDetail, self).form_invalid(form)

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_valid(form)

    def get_success_url(self):
        return reverse('posts:detail', kwargs={"pk": self.object.pk, "slug": self.object.slug})


class CategoryDetail(ListView):
    model = Post
    template_name = 'categories/category_detail.html'
    context_object_name = 'posts'
    paginate_by = 3

    @lru_cache(maxsize=None)
    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Post.objects.filter(category=self.category).order_by('-id')

    @lru_cache(maxsize=None)
    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        context['category'] = self.category
        return context


class TagDetail(ListView):
    model = Post
    template_name = 'tags/tag_detail.html'
    context_object_name = 'posts'
    paginate_by = 3

    @lru_cache(maxsize=None)
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.using('posts').filter(tag=self.tag).order_by('id')

    @lru_cache(maxsize=None)
    def get_context_data(self, **kwargs):
        context = super(TagDetail, self).get_context_data(**kwargs)
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        context['tag'] = self.tag
        return context


@method_decorator(login_required(login_url='users/login'), name="dispatch")
class CreatePostView(CreateView):
    template_name = 'posts/create-post.html'
    form_class = PostCreationForm
    model = Post

    def get_success_url(self):
        post = get_object_or_404(Post, id=self.object.pk)
        if post.image.width <= 450 and post.image.height <= 540:
            post.slider_post = True
        post.save(using='posts')
        return reverse('posts:detail', kwargs={"pk": self.object.pk, "slug": self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save(commit=False)

        tags = self.request.POST.get("tag").split(",")

        for tag in tags:
            current_tag = Tag.objects.using('posts').filter(slug=slugify(tag))
            if current_tag.count() < 1:
                create_tag = Tag.objects.using('posts').create(title=tag)
                form.instance.tag.add(create_tag)
            else:
                existed_tag = Tag.objects.using('posts').get(slug=slugify(tag))
                print(existed_tag)
                form.instance.tag.add(existed_tag)
        return super(CreatePostView, self).form_valid(form)


@method_decorator(login_required(login_url='users/login'), name="dispatch")
class UpdatePostView(UpdateView):
    model = Post
    template_name = 'posts/post-update.html'
    form_class = PostUpdateForm

    def get_success_url(self):
        return reverse('posts:detail', kwargs={"pk": self.object.pk, "slug": self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.tag.clear()

        tags = self.request.POST.get("tag").split(",")

        for tag in tags:
            current_tag = Tag.objects.using('posts').filter(slug=slugify(tag))
            if current_tag.count() < 1:
                create_tag = Tag.objects.using('posts').create(title=tag)
                form.instance.tag.add(create_tag)
            else:
                existed_tag = Tag.objects.using('posts').get(slug=slugify(tag))
                form.instance.tag.add(existed_tag)
        return super(UpdatePostView, self).form_valid(form)

    @lru_cache(maxsize=None)
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(UpdatePostView, self).get(request, *args, **kwargs)


@method_decorator(login_required(login_url='users/login'), name="dispatch")
class DeletePostView(DeleteView):
    model = Post
    success_url = '/'
    template_name = 'posts/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect(self.success_url)

    @lru_cache(maxsize=None)
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(DeletePostView, self).get(request, *args, **kwargs)


class SearchView(ListView):
    model = Post
    template_name = 'posts/search.html'
    paginate_by = 5
    context_object_name = 'posts'

    @lru_cache(maxsize=None)
    def get_queryset(self):
        query = self.request.GET.get("q")

        if query:
            return Post.objects.using('posts').filter(Q(title__icontains=query) |
                                       Q(content__icontains=query) |
                                       Q(tag__title__icontains=query)
                                       ).order_by('id').distinct()

        return Post.objects.using('posts').all().order_by('id')


@login_required()
def CreateArchiveView(request, *args, **kwargs):
    emailDetail = Post.objects.using('posts').get(id=kwargs['pk'])
    copyEmailDetail = Archive()
    for field in emailDetail.__dict__.keys():
        copyEmailDetail.__dict__[field] = emailDetail.__dict__[field]
    copyEmailDetail.main_user = User.objects.using('users').get(id=request.user.id)
    copyEmailDetail.save()
    return redirect('/')


@method_decorator(login_required(login_url='users/login'), name="dispatch")
class PostDetailArchive(DetailView, FormMixin):
    template_name = 'posts/detail_archive.html'
    model = Post
    context_object_name = 'single'
    form_class = CreateCommentForm

    @lru_cache(maxsize=None)
    def get(self, request, *args, **kwargs):
        self.hit = Post.objects.using('posts').filter(id=self.kwargs['pk']).update(hit=F('hit') + 1)
        return super(PostDetailArchive, self).get(request, *args, **kwargs)

    @lru_cache(maxsize=None)
    def get_context_data(self, **kwargs):
        context = super(PostDetailArchive, self).get_context_data(**kwargs)
        context['previous'] = Post.objects.using('posts').filter(id__lt=self.kwargs['pk']).order_by('-pk').first()
        context['next'] = Post.objects.using('posts').filter(id__gt=self.kwargs['pk']).using('posts').order_by('pk').first()
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.instance.post = self.object
            form.save()
            return super(PostDetailArchive, self).form_valid(form)
        else:
            return super(PostDetailArchive, self).form_invalid(form)

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_valid(form)

    def get_success_url(self):
        return reverse('posts:detail', kwargs={"pk": self.object.pk, "slug": self.object.slug})


@login_required(login_url='users/login')
def post_like(request, pk):
    post = get_object_or_404(Post, id=pk)
    slug = post.slug
    if post.likes.using('posts').filter(id=request.user.id).exists():
        post.likes.using('posts').remove(request.user)
    else:
        post.likes.using('posts').add(request.user)
    return HttpResponseRedirect(reverse('posts:detail', kwargs={"pk": pk, "slug": slug}))
