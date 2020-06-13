from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import CommentForm
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

class PostList(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.order_by('-created')

class PostSearch(PostList):
    def get_queryset(self):
        q = self.kwargs['q']
        object_list = Post.objects.filter(Q(title__contains=q) | Q(content__contains=q))
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostSearch, self).get_context_data()
        context['search_info'] = 'Search: {}'.format(self.kwargs['q'])
        return context

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

def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    post = comment.post
    if request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url()+'#comment-list')
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