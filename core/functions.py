import requests
import math

def download(url, num_retries=3):
  page = None
  try:
    response = requests.get(url)
    page = response.text
    if response.status_code >= 400:
      print ('Download error:', response.text)
      if num_retries and 500 <= response.status_code < 600:
        return download(url, num_retries - 1)
  except requests.exceptions.RequestException as e:
    print ('Download error:', e.reason)
  return page

def write_movie_CSV(movie, weekend_value, gross_value, weeks):
  with open("core/static/movies.csv", "a") as csv_file:
    csv_file.write(movie + ", " + weekend_value + ", " + gross_value + ", " + weeks + "\n")

def write_worldcup_CSV(name, value):
  with open("core/static/brazil_worldcup.csv", "a") as csv_file:
    csv_file.write(name + ", " + value + "\n")

def convert_to_float(text):
  if ("." in text and "," in text):
    return float(text.replace(".", "").replace(",", "."))
  elif ("." in text):
    return float(text.replace(".", ""))
  else:
    return float(text.replace(",", ""))

def millify(n):
  millnames = ['', ' mil', ' mi', ' bi']

  n = float(n)
  millidx = max(0,min(len(millnames)-1, int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

  return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])