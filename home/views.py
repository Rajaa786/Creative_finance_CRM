from django.shortcuts import render
from stronghold.decorators import public

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@public
def home(request):
        return render(request, 'home/home.html')

@public
def page_not_found_view(request, exception):
        return render(request, 'home/404.html', status=404)