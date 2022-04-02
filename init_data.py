""""
File of constants to be used in other files.
"""

CSV_FILE_NAME = 'wikipedia_ukraine_and_russia_network.csv'

BASE_VALUES = {'Russia', 'Ukraine'}

DATES_FOR_CHECKING = [
  ('20180401', '20180501'),
  ('20180501', '20180601'),
  ('20190901', '20191001'),
  ('20191001', '20191101'),
  ('20220101', '20220201'),
  ('20220201', '20220301')
]

DATES_STRINGS = [f'{pair[0]}-{pair[1]}' for pair in DATES_FOR_CHECKING]

COLUMNS = [
    'value',
    'ukraine_relevance',
    'russia_relevance',
    'pointers'
  ] + DATES_STRINGS

NUMBER_OF_VALUES = 10000