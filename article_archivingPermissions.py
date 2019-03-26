# -- coding: utf-8 --
import csv, sys

def read_file_get_list_of_dicts(infile_path):
    """
    __Args__
    1. infile_path (str): The path to the input file
    __Returns__
    * out_rows (list): A list of dictionaries populated with the existing
        csv data
    """
    out_rows = []

    with open(infile_path, mode='rU', errors='ignore') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            out_rows.append(row)
    return out_rows

def write_list_of_dicts_to_file(outfile_path, out_rows, field_names):
    """
    __Args__
    1. outfile_path (str): The path to the output file
    2. out_rows (list): A list of dictionaries containing data
    3. field_names (list): A list of strings containing field names
        which are present in EVERY dictionary in the out_rows array
    """

    with open(outfile_path, 'w') as resultsFile:
        field_names=['Publication_Type','Authors','Article_Title','Journal_Title','ISSN','EISSN','Publisher','Journal_Archiving_Version_Permissions','Embargo','Notes','DOI',
                    'Pubmed','Keywords','Abstract','Author_Affiliation','Reprint_Author','Email','Sponsors',
                    'Publication_Date','Publication_Year']


        writer = csv.DictWriter(resultsFile, field_names, extrasaction='ignore',lineterminator='\n')
        writer.writeheader()
        for out_row in out_rows:
            writer.writerow(out_row)

def get_version_and_embargo_data_and_notes(rows):
    data_dict = {}
    for row in rows:
        data_dict[row['ISSN']] = [row['Journal Version'], row['Embargo'], row['Notes']]
    return data_dict

def map_headers(old_row):

    mapping = {
        'PT': 'Publication_Type',
        'AF': 'Authors',
        'TI': 'Article_Title',
        'SO': 'Journal_Title',
        'SN': 'ISSN',
        'EI': 'EISSN',
        'PU': 'Publisher',
        'Journal_Archiving_Version_Permissions': 'Journal_Archiving_Version_Permissions',
        'DI': 'DOI',
        'PM': 'Pubmed',
        'DE': 'Keywords',
        'AB': 'Abstract',
        'C1': 'Author_Affiliation',
        'RP': 'Reprint_Author',
        'EM': 'Email',
        'FU': 'Sponsors',
        'PD': 'Publication_Date',
        'PY': 'Publication_Year',
        'Embargo': 'Embargo',
        'Notes': 'Notes'
        }

    new_row = {}
    for x in old_row:
        if x in mapping.keys():
            new_row[mapping[x]] = old_row[x]
        # else:
        #     print(x + " not in " + str(mapping.keys()))

    return new_row

def main():
    # Grab our infile_path and outfile_path from the cli
    infile_path = sys.argv[1]
    master_infile = sys.argv[2]
    outfile_path = sys.argv[3]

    wosrows = read_file_get_list_of_dicts(infile_path)

    mfrows = read_file_get_list_of_dicts(master_infile)

    mf = get_version_and_embargo_data_and_notes(mfrows)
    # print(mf)

    for row in wosrows:
        extra_info = mf.get(row['SN'], None)
        #print(extra_info)
        if extra_info is not None:
            row['Journal_Archiving_Version_Permissions'] = extra_info[0]
            row['Embargo'] = extra_info[1]
            row['Notes'] = extra_info[2]
            # print(row['Notes'])

        else:
            row['Journal_Archiving_Version_Permissions'] = 'NA'
            row['Embargo'] = 'NA'
            row['Notes'] = 'NA'
            # print(row)


    output_rows = [map_headers(x) for x in wosrows]

    fields_in_output = output_rows[0].keys()

    write_list_of_dicts_to_file(outfile_path, output_rows, fields_in_output)

    

if __name__ == '__main__':
    main()
