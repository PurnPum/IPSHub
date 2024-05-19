from django.shortcuts import render

# Create your views here.

def patches_list(request):
    return render(request, 'patches/patches.html')