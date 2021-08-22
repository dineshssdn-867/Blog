from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic import ListView
from myarchive.models import Archive
from posts.models import Post


@method_decorator(login_required(login_url='/users/login'), name="dispatch")
class ArchiveView(ListView):
    model = Archive
    template_name = 'Archive/archive.html'
    context_object_name = 'archives'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArchiveView, self).get_context_data(**kwargs)
        context['archives'] = Archive.objects.filter(main_user=self.request.user)
        context['posts'] = Post.objects.all()
        context['slider_posts'] = Archive.objects.all().filter(slider_post=True).order_by('id')
        return context
