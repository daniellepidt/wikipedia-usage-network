import os.path
import pandas as pd
from get_wiki_info import get_value_info
from init_data import CSV_FILE_NAME, BASE_VALUES, DATES_STRINGS, NUMBER_OF_VALUES


if os.path.isfile(CSV_FILE_NAME):
  values_df = pd.read_csv(CSV_FILE_NAME, index_col=0)
else:
  c = [
    'value',
    'ukraince_relevance',
    'russia_relevance',
    'pointers'
  ] + DATES_STRINGS
  values_df = pd.DataFrame(columns=c)
  values_df.to_csv(CSV_FILE_NAME)

checked_values = set(values_df['value'].to_list())

# Effort to speed up the gathering process:
# TODO: Make values_for_checking into a list of sets,
# and then add the new pointers set to the list after
# deducting the checked_values from it.
# That way I'll be able to go over the list by a more relevant order
# and also prevent the need to reindex the current way values_for_checking
# acts as a set with every new value added to it.

try:
  gathered_pointers = values_df['pointers'].to_list()
  values_for_checking = set()
  for p in gathered_pointers:
    p_set_of_values = set(p.split(', '))
    values_for_checking.update(p_set_of_values)
except Exception as e:
  print(e)
  values_for_checking = set()

index = 0

for value in BASE_VALUES:
  if value not in checked_values:
    values_df = get_value_info(values_for_checking, value, checked_values, values_df)

while values_for_checking and len(checked_values) <= NUMBER_OF_VALUES:
  # TODO: Create a mechanisem which can loop on the sets inside of the
  # values_for_checking list.
  value = values_for_checking.pop() # 
  values_df = get_value_info(values_for_checking, value, checked_values, values_df)
  current_index = len(checked_values)
  if current_index % 100 == 0:
    print(f'Reached {current_index} values in DB, saving!')
    values_df.to_csv(CSV_FILE_NAME)

values_df.to_csv(CSV_FILE_NAME)
print('Done!')