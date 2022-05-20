# wikipedia-usage-network
A project @ Complex Networks.

=====ATTENTION=====

In order to properly run the project's files, you're required
to create your own virutal environment please open a command line
in the root directory of this project and run the following commands:
1. python -m venv venv
2. venv/Scripts/activate
3. pip install -r requirements.txt
After performing all of these actions, you will have the same development
enviorment as we have, and everything should run smoothly.

For more information regarding Virtual Environments, please read:
https://docs.python.org/3/library/venv.html


====INSTRUCTIONS====

In order to start the scraping process, please run wikimedia_data_fetcher.py.
If you'd like to change the scrapings base settings and get different results
from what we used in our project, please change the constant inside of the
init_data.py file.

====================

The project contains the following files and directories:

01_initial_dbs: DBs which we have gathered from Wikipedia with different
versions of our code.

02_manual_work_dbs: DBs after first phase of processing. We unified the
different scrape results we've got, and removed those which have no
relevance for our subject of research- Ukraine & Russia.

03_clean_dbs: This DB only contains unique values with aggregated pageviews
from former similiar values which all lead to the same Wikipedia page.

04_graph_dbs: This DB contains the files used to create the graphs in Gephi,
using NetworkX.

05_most_relevant_db: This DB has the most relevant results from our clean DB,
in order to have a comprehensible graph in Gephi.

06_graph_datasets: This directory contains a Jupyter Notebook used to generate
the CSVs containing the datasets to be used in Gephi & two Jupyter Notebooks
used to calculate different properties of the our graphs using NetworkX.

gephi_files: This directory contains the Gephi files created in the work process.

pics_for_pdf: A file with Pandas plots outputed for usage in our final report.

venv: Virtual environment folder, containing all required packages to run the project.