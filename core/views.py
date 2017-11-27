import csv
import time
from django.http import HttpResponse
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from .functions import *
from .models import *

def index(request):
  return render(request, 'index.html')

def q1(request):
  url = "https://www.rottentomatoes.com/browse/tv-list-1"
  soup = BeautifulSoup(download(url), 'html5lib')
  table = soup.find_all('table')
  movies = table[0].find_all('tr')
  print(movies)
  movie_list = list()

  for m in movies:
    title = m.find(class_='middle_col').find('a').text
    score = m.find(class_='left_col').find('a').text
    movie_list.append({'title': title, 'score': score})

  return render(request, 'q1.html', {'movie_list': movie_list})

def q2(request):
  open("core/static/movies.csv", "w").truncate()

  url = "http://www.imdb.com/chart/boxoffice"
  soup = BeautifulSoup(download(url), 'html5lib')
  table = soup.find_all('tbody')
  movies = table[0].find_all('tr')
  movie_list = list()

  for m in movies:
    weekend_value = ""
    gross_value = ""
    title = m.find(class_='titleColumn').text.strip()
    values = m.find_all(class_='ratingColumn')
    for i in range(0, 2):
      if (i == 0):
        weekend_value = values[i].text.strip()
      else:
        gross_value = values[i].text.strip()
    weeks = m.find(class_='weeksColumn').text
    movie_list.append({'title': title, 'weekend_value': weekend_value, 'gross_value': gross_value, 'weeks': weeks})
    write_movie_CSV(title, weekend_value, gross_value, weeks)

  return render(request, 'q2.html', {'movie_list': movie_list})

def q3(request):
  url = "https://www.climatempo.com.br/previsao-do-tempo/cidade/264/teresina-pi"
  soup = BeautifulSoup(download(url), 'html5lib')
  max = soup.find("div", attrs={"class": "left border-bot small-12"}).find("p", attrs={"id": "tempMax0"}).text
  min = soup.find("div", attrs={"class": "left small-12"}).find("p", attrs={"id": "tempMin0"}).text
  rain_probability = soup.find("div", attrs={"class": "columns small-12 medium-6 top10"}).find("p", attrs={"arial-label": "ícone do tempo Manhã"}).text.split("m")[2]

  while WeatherForecast.objects.all().count() > 5:
    WeatherForecast.objects.order_by('id')[0].delete()

  forecasts = WeatherForecast.objects.all()[::-1]

  wf = WeatherForecast()
  wf.max = max
  wf.min = min
  wf.rain_probability = rain_probability
  wf.save()

  return render(request, 'q3.html', {'max': max, 'min': min, 'rain_probability': rain_probability, 'forecasts': forecasts})

def q4(request):
  base_url = "http://example.webscraping.com"
  page_url = "/places/default/index/%d"
  countries = list()
  country_list = list()

  for page in range(26):
    if page == 0:
      url = base_url
    else:
      url = (base_url + page_url) % page
    soup = BeautifulSoup(download(url), 'html5lib')
    for country in soup.find_all("td"):
      countries.append(country.find('a')['href'])
    time.sleep(1)

  for country in countries:
    url = base_url + country
    soup = BeautifulSoup(download(url), 'html5lib')
    name = soup.find("tr", attrs={"id": "places_country__row"}).find(class_="w2p_fw").text
    area = convert_to_float(soup.find("tr", attrs={"id": "places_area__row"}).find(class_="w2p_fw").text.split(" ")[0])
    population = convert_to_float(soup.find("tr", attrs={"id": "places_population__row"}).find(class_="w2p_fw").text)
    if area > 0:
      density = population / area
    else:
      density = 0
    country_list.append({'name': name, 'area': str(int(area)) + ' km²', 'population': str(int(population)), 'density': str('%.2f person/km²') %density})
    time.sleep(1)

  return render(request, 'q4.html', {'country_list': country_list})

def q5_6(request):
  open("core/static/brazil_worldcup.csv", "w").truncate()

  url = "http://www.portaltransparencia.gov.br/copa2014/api/rest/empreendimento"
  soup = BeautifulSoup(download(url), 'xml')

  all_values = soup.find_all('valorTotalPrevisto')
  values = list()
  for value in all_values:
    values.append(float(value.text))
  total_value = sum(values)

  ventures = list()
  for doing in soup.find_all('copa:empreendimento'):
    id = int(doing.cidadeSede.id.text)
    name = doing.cidadeSede.descricao.text
    if doing.valorTotalPrevisto:
      value = float(doing.valorTotalPrevisto.text)
      ventures.append({"id": id, "name": name, "value": value})
    else:
      ventures.append({"id": id, "name": name, "value": 0})

  cities = list()
  for id in range(1, 15):
    total = 0.0
    name = ""
    for doing in ventures:
      if doing['id'] == id:
        if name == "":
          name = doing['name']
        total += doing['value']
    cities.append({"name": name, "value": "R$ " + millify(total)})
    write_worldcup_CSV(name, str("%.2f" %total))

  write_worldcup_CSV("Total", str("%.2f" %total_value))

  return render(request, "q5_6.html", {"total": "R$ " + str(millify(total_value)), "cities": cities})