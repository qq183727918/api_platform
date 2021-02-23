from django.shortcuts import render


# Create your views here.

def welcome(request):
    return render(request, 'welcome.html')


def case_list(request):
    return render(request, 'case_list.html')


def home(request):
    return render(request, 'home.html')