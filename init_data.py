""""
File of constants to be used in other files.
If you'd like to get different results when running
wikimedia_data_fetcher.py, change the constants here
beforehand.
"""

# Name of the output file:
CSV_FILE_NAME = 'wikipedia_ukraine_and_russia_network.csv'

# The values the scrape will start with:
BASE_VALUES = {'Russia', 'Ukraine'}

# The date pairs that will be checked by the pageviewsapi.
# Please not that the pairs should be of a month's timeframe.
DATES_FOR_CHECKING = [
  ('20180401', '20180501'),
  ('20180501', '20180601'),
  ('20190901', '20191001'),
  ('20191001', '20191101'),
  ('20220101', '20220201'),
  ('20220201', '20220301')
]

# Create a list of strings, that will be later used in creating
# the columns of the DataFrame.
DATES_STRINGS = [f'{pair[0]}-{pair[1]}' for pair in DATES_FOR_CHECKING]

# List of all columns' names:
COLUMNS = [
    'value',
    'ukraine_relevance',
    'russia_relevance',
    'pointers'
  ] + DATES_STRINGS

# Number of values at which the scraping process should stop:
NUMBER_OF_VALUES = 10000