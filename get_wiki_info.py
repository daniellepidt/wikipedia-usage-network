from requests import get
from bs4 import BeautifulSoup
from re import findall
import pageviewapi
from init_data import DATES_FOR_CHECKING, DATES_STRINGS

def get_pointers(p_tags):
  """
  This function is used to find all of the pointers to other
  Wikipedia pages which are present in
  each value we check.
  Starts with the HTML <p> (paragraph) tags
  which hold all of the relevant text on the
  Wikipedia page.
  """
  pointers = []
  for p in p_tags:
    # Get all <a> (anchor) tags which are links.
    p_links = p.find_all('a')
    for pl in p_links:
      # Get the title field, which is used to 
      # identify the next value.
      title = pl.get('title')
      # Clean irrelevant <a> tags & junk.
      if title != None and ':' not in title and '.' not in title and len(title) > 1:
        pointers.append(title)

  # Return as a set of unique values.
  return set(pointers)

def find_relevance(p_tags):
  """
  This function finds the number of mentions
  of 'ukr' & 'russ' in each Wikipedia page,
  under the assumptions that these are substrings
  which will be used in words which are relevant to 'Ukraine' & 'Russia'.
  Starts with the HTML <p> (paragraph) tags
  which hold all of the relevant text on the
  Wikipedia page.
  """
  text_p = ' '.join([p.text.lower() for p in p_tags]) # Joins all text into one string of lowercase text.
  ukr = text_p.count('ukr') # Count occurrences of 'ukr'.
  russ = text_p.count('russ') # Count occurrences of 'russ'.
  return {
    'ukraine_relevance': ukr,
    'russia_relevance': russ
  }

def get_pageviews(value):
  """"
  This function uses the pageviewapi package
  in order to easily query the Wikimedia's API
  and retrieve pageviews data from it.
  """
  wiki = 'en.wikipedia'
  pageviews = {}
  for i in range(len(DATES_STRINGS)):
    # The loop gets information for every pair of
    # dates given to it.
    try:
      pageviews[DATES_STRINGS[i]] = pageviewapi.per_article(wiki, value, DATES_FOR_CHECKING[i][0], DATES_FOR_CHECKING[i][1], granularity='monthly')['items'][0]['views']
    except Exception as e:
      # If the Wikipedia page didn't exist at
      # the dates requested, the API returns
      # an error. In such a case - we save
      # a 'None' value in order to prevent
      # the script from crashing.
      pageviews[DATES_STRINGS[i]] = None
  return pageviews

def get_p_tags(value):
  url = f'https://en.wikipedia.org/wiki/{value.replace(" ", "_")}'
  content = get(url).content # Get HTML page content with HTTP request.
  soup = BeautifulSoup(content, 'html.parser') # Parser HTML content.
  p_tags = soup.find_all('p') # Get all <p> (paragraph) tags.
  return p_tags

def get_value_info(values_for_checking, value, checked_values, values_df):
  """
  This function contains the whole process of getting values
  with the rest of the functions above.
  It returns an updated dataframe containing the new value.
  """
  p_tags = get_p_tags(value) # Get all <p> (paragraph) tags.
  pointers = get_pointers(p_tags)
  relevance = find_relevance(p_tags)
  
  values_for_checking.append(pointers) # Add the new pointers to the list of sets.

  pointers_string = ', '.join(list(pointers)) # Turn into string for easier saving to DF.
  pageviews = get_pageviews(value)
  print(f'Checking {value}: UKR -  {relevance["ukraine_relevance"]} | RUSS - {relevance["russia_relevance"]}') # Print to show progress to the user.
  checked_values.add(value) # Add the value to the set in order to prevent redundant checks.
  d = {
    'value': value,
    'pointers': pointers_string,
    **relevance,
    **pageviews
  }
  return values_df.append(d, ignore_index=True) # Return the new DF with the added line.