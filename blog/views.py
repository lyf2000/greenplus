import datetime

from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from .tasks import remind_meets
# Create your views here.
from django.views.generic import DetailView, ListView

from blog.api.filters import PostFilter
from blog.forms import PostForm, MeetForm
from blog.models import Meet, Post

TIMEDELTA_WITH_UTC_ERROR = datetime.timedelta(hours=3)

# def index(request):
#     if request.is_ajax():
#         print('AJAX')
#         coords = ast.literal_eval(request.POST.get('coords', None))
#         return JsonResponse({'data': 'OK'})
#
#     return render(request, 'blog/index.html')


# def post_list(request):
#     f = PostFilter(request.GET, queryset=Post.objects.all())
#     return render(request, 'blog/post_list.html', {'filter': f})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


def meet_detail(request, pk):
    try:
        meet = Meet.objects.get(id=pk)
    except Meet.DoesNotExist as e:
        raise e
    return render(request, 'blog/meet_detail.html', {'meet': meet})


class MeetListView(ListView):
    model = Meet
    template_name = 'blog/meet_list.html'


class PostListView(ListView):
    model = Post
    template_name = 'blog/post-list.html'


# def post_detail(request, pk):
#     try:
#         post = Post.objects.get(id=pk)
#     except Post.DoesNotExist as e:
#         raise e
#     return render(request, 'blog/post_detail.html', {'meet': post})

@login_required
def meet_create(request):
    if request.method == 'POST':
        meet = MeetForm(request.POST)
        if meet.is_valid():
            meet = meet.save()
            remind_meets.apply_async(args=(meet.pk,), eta=meet.meet_date - TIMEDELTA_WITH_UTC_ERROR - datetime.timedelta(hours=1))
    form = MeetForm()
    return render(request, 'blog/meet_create.html', {'form': form})


class BookForm(forms.ModelForm):
    """
    Your `forms.ModelForm` subclass representing the `Book` model directly.
    """

    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'main_img']


@login_required
def post_create(request):
    if request.method == 'POST':
        post = PostForm(request.POST, request.FILES)
        if post.is_valid():
            post.save()

        else:
            context = {}
            context['form'] = post
            return render(request, 'blog/post_create.html', context)
    form = PostForm(initial={'author': request.user})
    context = {
        'form': form
    }

    return render(request, 'blog/post_create.html', context)


def e_handler404(request, exception):
    context = RequestContext(request)
    response = render_to_response('404.html', context)
    response.status_code = 404
    return response

def e_handler500(request):
    return render(request,'500.html')