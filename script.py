# -*- coding: utf-8 -*-
import pandas as pd
import json

def load_data_on_dictionaries(df1_xlsx, df2_xls):
    # Create list of dictionaries from XLSX file1
    rows1 = []
    for index, row in df1_xlsx.iterrows():
        rows1.append({
            'date': row[0],
            'code': row[3],
            'client_name': row[8],
            'total': row[15]
        })
    # Create list of dictionaries from XLS file2 
    rows2 = []
    for index, row in df2_xls.iterrows():
        rows2.append({
            'date': row[1],
            'code': row[3],
            'client_name': row[5],
            'total': row[17]
        })
    
    return rows1, rows2


def equalize_data_types(rows):
    #clean data of the row of dictionaryes so they have the same format
    for row in rows:
        # Convert 'date' key to datetime object
        if isinstance(row['date'], pd.Timestamp):
            row['date'] = row['date'].strftime('%d/%m/%Y')
       
        # Convert 'code' key to string format
        row['code'] = str(row['code'])[-3:]
        row['code'] = row['code'].lstrip('0')
       
        # Sort 'client_name' words for comparison
        client_name_words = row['client_name'].split()
        sorted_words = ' '.join(sorted(client_name_words))
        row['client_name'] = sorted_words   
        
        # Convert 'total' key to absolute value
        row['total'] = abs(row['total'])
        
    return rows


def search_non_matching_dicts(rows1, rows2):
    unmatched_rows = []

    for d1_row in rows1:
        match_found = False

        for d2_row in rows2:
            if json.dumps(d1_row, sort_keys=True) == json.dumps(d2_row, sort_keys=True):
                match_found = True
                break

        if not match_found:
            unmatched_rows.append(d1_row)

    return unmatched_rows


def main():
    #load the two files to compare
    df1_xlsx = pd.read_excel('file1.xlsx', header=1) #AFIP
    df2_xls = pd.read_excel('file2.xlsx') #XUBIO
    
    #load data of the two files in two rows of dictionaries
    rows1, rows2 = load_data_on_dictionaries(df1_xlsx, df2_xls)
    
    #clean the data on them so they have the same format
    processed_row1 = equalize_data_types(rows1)
    processed_row2 = equalize_data_types(rows2)
    
    # search for the dictionares of the first file(AFIP) that AREN'T on the second file(Xubio) 
    non_matching_dicts = search_non_matching_dicts(processed_row1, processed_row2)
    
    #then show them OR "All match" in case all of them are in the second file
    if non_matching_dicts:
        print("Afip rows that are not on Xubio:")
        for d in non_matching_dicts:
            print(d)
    else:
        print("All Afip Rows are found on Xubio")


if __name__ == "__main__":

    main()
    
    
    