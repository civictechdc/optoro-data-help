#!/usr/bin/env python3

"""This script will load the spreadsheets in Workplans.zip, add columns
with metadata from the file names, and save a concatenated CSV called
workplans.zip.
"""

import re
from os import remove
from zipfile import ZipFile
import pandas as pd

FILENAME_PATTERN = (r'(?P<Year>\d{4})_(?P<Org_Code>.*?)_workplan?&budget.xls.'
                    'Project_Proposals(?:-(?P<Proposal_Number>\d+))?.csv')


def parse_filename_to_columns(df, filename):
    """Parse the provided filename and add results as columns
    to the given DataFrame.
    """
    for col, val in re.search(FILENAME_PATTERN, filename).groupdict().items():
        df[col] = val
    return df


def snake_case_column_names(df):
    """Convert column names to snake case."""
    df.columns = [re.sub(r'\s+', '_', col.lower()) for col in df.columns]
    return df


def load_dfs(filenames):
    """Load the provided filenames, parse filenames to year, org_code,
    and proposal_number columns, concatenate the data, convert other
    column names to snake case, and return the resulting DataFrame.
    """
    dfs = {'%s.%s' % (filename, sheet): df for filename in filenames
           for sheet, df in pd.read_excel(filename, sheet_name=None).items()}
    return pd.concat([df.pipe(parse_filename_to_columns, filename)
                      for filename, df in dfs.items()])


def extract_workplans(zip_path='./Workplans.zip'):
    """Extract the files in the provided zip_path (default
    './Workplans.zip') and return a list of extracted files.
    """
    with ZipFile(zip_path) as archive:
        archive.extractall('/tmp/')
        return ['/tmp/%s' % filename for filename in archive.namelist()]


def delete_extracted(namelist):
    """Delete the given files."""
    for filename in namelist:
        remove(filename)


def main():
    """Execute script."""
    filenames = extract_workplans()
    load_dfs(filenames)\
        .to_csv('workplans.csv', index=False)



if __name__ == '__main__':
    main()
