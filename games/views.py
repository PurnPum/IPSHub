from django.shortcuts import render

# Create your views here.

def games_list(request):
    return render(request, 'games/games_sidebar_layout.html')