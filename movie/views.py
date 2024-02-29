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
from .models import Movie  # Adjust this import based on your project's structure
from collections import defaultdict

def statistics_view(request):
    # Fetch all movies
    movies = Movie.objects.all()
    
    movie_counts_by_primary_genre = defaultdict(int)  # Use defaultdict to automatically initialize counts

    # Process each movie to extract its primary genre
    for movie in movies:
        genres = movie.genre.split(',')  # Assuming genres are separated by commas
        if genres:  # Check if there's at least one genre
            primary_genre = genres[0].strip()  # Get the first genre and strip any leading/trailing whitespace
            movie_counts_by_primary_genre[primary_genre] += 1
        else:
            movie_counts_by_primary_genre['None'] += 1  # Handle movies without a genre

    # Prepare data for plotting
    genres = list(movie_counts_by_primary_genre.keys())
    counts = list(movie_counts_by_primary_genre.values())
    bar_positions = range(len(genres))
    
    # Create the bar chart
    plt.figure(figsize=(10, 8))  # Adjust the figure size as needed
    plt.bar(bar_positions, counts, width=0.5, align='center')
    
    # Customize the chart
    plt.title('Pelis por genero')
    plt.xlabel('Primary Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions, genres, rotation=90)
    
    # Adjust layout
    plt.tight_layout()  # Use tight_layout to automatically adjust subplot parameters
    
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
    
    # Render the template statistics.html with the chart
    return render(request, 'statistics.html', {'graphic': graphic})
