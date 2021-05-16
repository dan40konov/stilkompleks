from django.shortcuts import render
from django.http import HttpResponse


posts = [
    {
        'author': 'Author1',
        'title': 'Title 1',
        'content': 'Content Post 1',
        'date_posted': '11/11/1911'

    },
    {
        'author': 'Author2',
        'title': 'Title 2',
        'content': 'Content Post 2',
        'date_posted': '11/11/1912'

    }

]
# Create your views here.
def home(request):
    ctx = {
        'posts': posts
    }
    return render(request, 'dj_project/home.html', ctx)

# Create your views here.
def about(request):
    return render(request, 'dj_project/about.html')