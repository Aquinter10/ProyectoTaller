from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    # return render(request,'home.html')
    return render(request,'home.html',{'name':'Alejandro Quintero Moreno'})

def about(request):
    return HttpResponse('this is the about page')

