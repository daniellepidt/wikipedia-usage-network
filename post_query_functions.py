""""
This file contains functions which are
used to clean up the data and improve it
after finishing the query.
"""

import sys
import os
import pandas as pd
import numpy as np
from get_wiki_info import get_p_tags, find_relevance, get_pageviews
from init_data import DATES_STRINGS

def unify_similiar_values(df):
  """
  This function looks for values which have multiple names
  which all lead to the same Wikipedia page, and then unifies
  them and aggregates their number of pageviews.
  Examples of this can be the values of:
  'Ukrainian language' & 'Ukrainian Language'
  In order to know which lines to unify, we look for values which
  have identical values for both pointers and relevance fields.
  """
  # Create list of columns to group on:
  group_on = ['ukraine_relevance', 'russia_relevance', 'pointers']
  # Aggregation function which sums all date columns, while taking the first string from each group of similiar value rows:
  funcs = {col: 'sum' if col in DATES_STRINGS else 'first' for col in df.drop(group_on, axis=1).columns}
  # Create the new DF by grouping with as_index=False in
  # order to prevent the DF from dropping the group_on columns
  # in the aggregation process:
  new_df = df.groupby(group_on, as_index=False).agg(funcs).sort_values(by=['ukraine_relevance', 'russia_relevance'], ascending=False, ignore_index=True)

  # Pass the value column to the first column of the DF:
  values = new_df.pop('value')
  new_df.insert(0, 'value', values)

  return new_df

def add_all_missing_nodes_to_df(df):
  """
  This function runs over all of the collected pointers and
  indexes the ones which are missing from the data.
  This function is needed in order to ensure that we have
  all of the required nodes in the data.
  This function only gathers pageviews for the new nodes, without
  collecting their own new pointers.
  This is done in order to prevent an infinite process of
  needing to gather missing information, but instead defining
  this information as irrelevant to our current goal.

  !!! Leaving this function here for future use if needed !!!
  """
  # Get all values which were already checked:
  checked_values = set(df['value'])
  
  # Take the pointers column, turn it into a list of strings,
  # unify by the commas into one string, and then
  # split into one list & turn into a set.
  # Take the set, and deduct from it all checked_value
  # so you end up with a set of values which haven't been
  # checked yet:
  values_for_checking = set(", ".join(list(df['pointers'])).split(", ")) - checked_values
  # That way we end up with a set with one appearance of every value
  # which doesn't have a row for it in the DF.
  number_of_checks = len(values_for_checking)
  print(f'Missing {number_of_checks} values.')
  missing_values = []
  for (index, value) in enumerate(values_for_checking):
    p_tags = get_p_tags(value) # Get all <p> (paragraph) tags.
    relevance = find_relevance(p_tags)
    pageviews = get_pageviews(value)
    d = {
      'value': value,
      'pointers': '',
      **relevance,
      **pageviews
    }
    missing_values.append(d)
    print(f'{index} {value}: UKR -  {relevance["ukraine_relevance"]} | RUSS - {relevance["russia_relevance"]}') # Print to show progress to the user.
  missing_values_df = pd.DataFrame(missing_values)
  return missing_values_df

  df = get_value_info(values_for_checking, value, checked_values, df)


def remove_unexisting_pointers_from_nodes(df):
  """
  This function removes pointers which don't have appropriate
  rows in the DF. This is used to clean up the data, and only
  have the rows which are absolutely necessary.
  """
  # Get all values which were already checked:
  checked_values = set(df['value'])
  
  def leave_relevant_pointers(pointers_string):
    """
    Helper function:
    Takes the pointers string, turn it into a list of strings,
    then a set and make an intersection with checked_values.
    Then, turn the set back into a string.
    That leaves us only with values which were already checked.
    """
    return ", ".join(set(pointers_string.split(", ")) & checked_values)

  df['pointers'] = df['pointers'].apply(leave_relevant_pointers)
  return df
  

def main(args):
  csv_path = args[0]
  while True:
    # Check if a saved file under the name already exists.
    if os.path.isfile(csv_path):
      values_df = pd.read_csv(csv_path, index_col=0)
      break
    else:
      print('File doesn\'t exist at: ', csv_path)
      csv_path = input('Please input the correct file path: ')
  
  unified_df = unify_similiar_values(values_df)
  clean_df = remove_unexisting_pointers_from_nodes(unified_df)
  clean_df.to_csv(f'clean_{csv_path}', encoding='utf-8')

if __name__ == '__main__':
  main(sys.argv[1:])