""""
This file contains functions which were
intended to be used in order to create the data to be used
with NetoworkX & Gephi.

In the end, we performed the process with a
Jupyter Notebook under the same name as this file.
As such, this file was kept for documentation
purposes.
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
  network_df = pd.DataFrame() #for later
  ser_values = df.ix[:,0]
  ser_pointers = df.ix[:,3]
  ser_combined = ser_values.append(ser_pointers,ignore_index = True)
  ser_combined = ser_combined.unique()
  set_nodes = set(ser_combined)


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