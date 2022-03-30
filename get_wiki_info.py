from requests import get
from bs4 import BeautifulSoup
from re import findall
import pageviewapi
from init_data import DATES_FOR_CHECKING, DATES_STRINGS
import pdb as bkp

def get_pointers(p_tags):
  pointers = []
  for p in p_tags:
    p_links = p.find_all('a')
    for pl in p_links:
      title = pl.get('title')
      if title != None and ':' not in title and '.' not in title and len(title) > 1:
        pointers.append(title)

  return set(pointers)

def find_relevance(p_tags):
  text_p = ' '.join([p.text.lower() for p in p_tags])
  ukr = text_p.count('ukr')
  russ = text_p.count('russ')
  return {
    'ukraince_relevance': ukr,
    'russia_relevance': russ
  }

def get_pageviews(value):
  wiki = 'en.wikipedia'
  pageviews = {}
  for i in range(len(DATES_STRINGS)):
    try:
      pageviews[DATES_STRINGS[i]] = pageviewapi.per_article(wiki, value, DATES_FOR_CHECKING[i][0], DATES_FOR_CHECKING[i][1], granularity='monthly')['items'][0]['views']
    except Exception as e:
      pageviews[DATES_STRINGS[i]] = None
  return pageviews

def get_value_info(values_for_checking, value, checked_values, values_df):
  checked_values.add(value)
  current_index = len(checked_values)
  print(f'{current_index} - Checking {value}')
  url = f'https://en.wikipedia.org/wiki/{value.replace(" ", "_")}'
  content = get(url).content
  soup = BeautifulSoup(content, 'html.parser')
  p_tags = soup.find_all('p')
  pointers = get_pointers(p_tags)
  relevance = find_relevance(p_tags)
  
  values_for_checking.update(pointers - checked_values)
  pointers_string = ', '.join(list(pointers))
  pageviews = get_pageviews(value)
  d = {
    'value': value,
    'pointers': pointers_string,
    **relevance,
    **pageviews
  }
  return values_df.append(d, ignore_index=True)