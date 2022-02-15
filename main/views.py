from django.shortcuts import render
from django.http import HttpResponseRedirect

def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('dashboard')
    
    else:
        context = {}
        return render(request, 'main/index.html', context)