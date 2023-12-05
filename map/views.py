from django.shortcuts import render, redirect
import folium
import geocoder
from .models import Search
from .forms import SearchForm
from django.contrib import messages

def home(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = SearchForm()

    address = Search.objects.last()

    if address:
        location = geocoder.osm(address, language='en')

        if location.lat is not None and location.lng is not None:
            lat = location.lat
            lng = location.lng
            country = location.country

            m = folium.Map(location=[lat, lng], zoom_start=10, lang='en')
            folium.Marker([lat, lng], tooltip="click for more", popup=country).add_to(m)
            m = m._repr_html_()

            return render(request, 'index.html', {'m': m, 'form': form})
        else:
            address.delete()
            messages.success(request, 'Address is not valid')
            return redirect("/")
    else:
        messages.success(request, 'No address available.')

    return render(request, 'index.html', {'form': form})