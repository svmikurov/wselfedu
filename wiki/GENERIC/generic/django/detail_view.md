`view.py`
```
from django.views.generic import DetailView

from blog.models import Post


class UserPostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        queryset = Post.objects.get(pk=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context['blog_detail'] = queryset
        return context
```
или короче
```
class DiscussionDetailView(DetailView):
    model = Discussion
    template_name = 'discussions/detail.html'
    context_object_name = 'discussion_detail'
```