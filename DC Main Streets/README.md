## DC Main Street Management Documents

Management data for the Main Street Neighborhood Program. Requested during the Code for DC FOIA Party, receieved from Dept. of Small & Local Business Development.

## Cleaned data files

| original filename  | cleaned filename  | notes/q's  |
|---|---|---|
| Designation-Termination dates.xlsx  | designation_termination_dates_cleaned.csv  |  Combined the data across four tabs into one CSV for easier merging with the rest of the dataset. |
|  Historic Quarterly Reports.xlsx | dc_main_streets_quartery_summaries_cleaned.xlsx | There were several column names that didn't make sense, so the questions are in the comments in the definition tab. Some of the values of "average public investment" are negative and some are positive and it isn't clear what this means.  |
|  JOBS  BUSINESS STATS TABLE 2004-2012.xls  |   | We didn't understand the purpose of this file.  |
| Quarterly_Reports FY13-18.xls  |  | Cleaned up historical instead because there was more data.  |
| Workplans.zip  | workplans.csv  | munge_workplans.py is the script used to combine all the workplans into one. Abbreviation in column names are DSLBD: Dept. of Small & Local Business Development; CBE: certified business enterprises.|

A quick visualization of the historical [data](https://public.tableau.com/profile/mrgoynes#!/vizhome/DCMainStreetsQuarterlySummaries/SoSpotty?publish=yes).