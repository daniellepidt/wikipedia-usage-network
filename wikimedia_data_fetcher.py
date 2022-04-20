"""
Run this file in order to start scraping Wikipedia
and get the data you'd like to analyze.
Please take in consideration this is a lengthy process,
which may take several hours depending on the NUMBER_OF_VALUES
constant in the init_data.py file.
"""

import os.path
import pandas as pd
from get_wiki_info import get_value_info
from init_data import CSV_FILE_NAME, BASE_VALUES, DATES_STRINGS, COLUMNS, NUMBER_OF_VALUES

# Check if a saved file under the name already exists.
if os.path.isfile(CSV_FILE_NAME):
  values_df = pd.read_csv(CSV_FILE_NAME, index_col=0)
# If not - create a new dataframe.
else:
  values_df = pd.DataFrame(columns=COLUMNS)

# Get the dataframe's values and add id to checked_values set,
# in order to prevent redundant checks.
checked_values = set(values_df['value'].to_list())

# values_for_checking will use a list of sets.
values_for_checking = []

# Check the Wikipedia values of Russia & Ukraine first
# in order to make sure the most relevant info
# will surely be checked.
for value in BASE_VALUES:
  if value not in checked_values:
    values_df = get_value_info(values_for_checking, value, checked_values, values_df)

while values_for_checking and len(checked_values) <= NUMBER_OF_VALUES:
  set_of_pointers = values_for_checking.pop(0) - checked_values
  # Loop on the sets inside of the
  # values_for_checking list.
  for value in set_of_pointers:
    values_df = get_value_info(values_for_checking, value, checked_values, values_df)
    # Periodical save, in order to have a backup 
    # in the case on an exception.
    current_index = len(checked_values)
    if current_index % 100 == 0:
      print(f'Reached {current_index} values in DB, saving!')
      values_df.to_csv(CSV_FILE_NAME, encoding='utf-8')

# Save final result & finish.
values_df.to_csv(CSV_FILE_NAME, encoding='utf-8')
print('Done!')