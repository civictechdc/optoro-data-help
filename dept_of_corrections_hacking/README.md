# Dept of Corrections Data

Every week(this time is not fixed) departments of corrections post a pdftable on their site. The site URL changes based on the from date and to date they decide to post. This file is posted in a pdf format.

The notebook named `dept_of_corrections.ipynb` goes and queries all the dates in the past 2 years from 2016 and tries to get each and every file. The files in the pdftable format are in `weekly_corrections_data/pdf` . This data is slightly tricky to parse so the notebook makes use of an API which converts pdftables to excel files and post them as excel files in `weekly_corrections_data/excel` folder.
This excel files are further processed to convert them into csvs and stored under `weekly_corrections_data/csv` folder.

Note: To use pdftable api, you have to go to https://pdftables.com/pdf-to-excel-api and create a token as shown on the site. 