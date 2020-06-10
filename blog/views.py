from django.shortcuts import render, redirect
from .models import Post
from .forms import CommentForm
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

class PostList(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.order_by('-created')

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'content', 'head_image']

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = '__all__'

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated():
            form.instance.author = current_user
            return super(type(self), self).form_valid(form)
        else:
            return redirect('blog/')

def new_comment(request, pk):
    post = Post.objects.get(pk=pk)

    if(request.method == 'POST'):
        comment_form = CommentForm(request.POST)
        if(comment_form.is_valid()):
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(comment.get_absolute_url())
    else:
        return redirect('/blog/')


""" 
def post_detail(request, pk):
    blog_post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/post_detail.html',
        {
            'blog_post':blog_post,
        }
    )
"""

# Create your views here.
# def index(request):
#     posts = Post.objects.all()

#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts':posts,
#         }
#     )