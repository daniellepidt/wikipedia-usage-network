""""
This file contains functions which were
used in order to create the data to be used
with NetoworkX & Gephi.
"""

import sys
import os
import pandas as pd

def create_network_nodes_and_links(df):
  """
  This function will get a DF and output for every date:
  1. A nodes CSV file which will include every node's:
     1.1. ID
     1.2. Value
     1.3. Relevant date's pageviews
  2. A links CSV file which will include pairs of directed
     links from every value to it's pointers as described
     by their IDs.
  """


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
  
  

if __name__ == '__main__':
  main(sys.argv[1:])