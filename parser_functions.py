""""
This file contains functions which were
used in order to create the data to be used
with NetoworkX & Gephi.
"""

import os
import pandas as pd

def create_network_noded_and_links(csv_path):
  path = csv_path
  while True:
    # Check if a saved file under the name already exists.
    if os.path.isfile(path):
      values_df = pd.read_csv(path, index_col=0)
      break
    else:
      print('File doesn\'t exist at: ', path)
      path = input('Please input the correct file path: ')