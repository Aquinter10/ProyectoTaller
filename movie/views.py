from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie


import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
# Create your views here.

def home(request):
    # return render(request,'home.html')
    #return render(request,'home.html',{'name':'Alejandro Quintero Moreno'})
    searchTerm =request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies=Movie.objects.all()

    return render(request,'home.html',{'searchTerm':searchTerm,'movies':movies})


def signup(request):
    email=request.GET.get('email','')
    return render(request,'signup.html',{'email':email})




def about(request):
    return render(request,'about.html')


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render
from .models import Movie  
from collections import defaultdict

def statistics_view(request):
    # Fetch all movies
    movies = Movie.objects.all()
    
    movie_counts_by_primary_genre = defaultdict(int)  

    
    for movie in movies:
        genres = movie.genre.split(',') 
        if genres: 
            primary_genre = genres[0].strip()  
            movie_counts_by_primary_genre[primary_genre] += 1
        else:
            movie_counts_by_primary_genre['None'] += 1  

    
    genres = list(movie_counts_by_primary_genre.keys())
    counts = list(movie_counts_by_primary_genre.values())
    bar_positions = range(len(genres))
    
    
    plt.figure(figsize=(10, 8))  
    plt.bar(bar_positions, counts, width=0.5, align='center')
    
    
    plt.title('Pelis por genero')
    plt.xlabel('Primary Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions, genres, rotation=90)
    
    
    plt.tight_layout()  #
    
    # Save the chart to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    # Convert the chart to base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
 
    return render(request, 'statistics.html', {'graphic': graphic})
