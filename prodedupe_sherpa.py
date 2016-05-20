import csv
import sys
import requests
from xml.etree import ElementTree as ET
# from ET import Element, SubElement, Comment, tostring


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
        writer = csv.DictWriter(resultsFile, field_names)
        writer.writeheader()
        for out_row in out_rows:
            writer.writerow(out_row)


def main():
    # Grab our infile_path and outfile_path from the cli
    infile_path = sys.argv[1]
    outfile_path = sys.argv[2]

    # Specify our original fields
    original_fields = [
        "Author", "Department", "Title", "Year_Published",
        "DOI", "Journal", "Publisher", "Published_URL",
        "KUSW_URL", "Rights_to_Share", "Conditions",
        "SourceFile", "DuplicateHandle", "DuplicateDOI",
        "Crossref_author","Crossref_title","Crossref_journal",
        "Crossref_author","Crossref_issn"
        ]

    # Get our original data structure
    rows = read_file_get_list_of_dicts(infile_path)
    original_fields = [x for x in rows[0].keys()]

    # Manipulate that structure however we want, in this case I add another
    # column to everything called "brian_column" that has a random uuid in it
    sherpa_url = 'http://www.sherpa.ac.uk/romeo/api29.php'
    key='wSVmR3v9xnw'

    # Set a counter to print so we know how fast things are going
    i = 0
    m = len(rows)

    for row in rows:

        # increment our counter
        i += 1
        # print the counter
        # print("{}/{}".format(str(i), str(m)))

        issn = row['Crossref_issn']

        if len(issn) > 0:

            req = requests.get(sherpa_url+'?issn='+issn+'&ak='+key)

            root = ET.fromstring(req.text)

            #get number of hits
            for value in root.findall('header'):
                numhits=value.find('numhits')
                hits=numhits.text
                row['NumberOfHits'] = hits
            #get prearchiving archiving permissions
            for value in root.findall('publishers/publisher'):
                pa=value.find('preprints/prearchiving')
                if pa is None:pass
                else:
                    paText=pa.text
                    row['Prearchiving_permissions'] = paText

            #get prearchiving archiving restrictions
            for value in root.findall('publishers/publisher'):
                pr=value.find('preprints/prerestrictions')
                if pr is None:pass
                else:
                    prText=pr.text
                    row['Prearchiving_restrictions'] = prText


            #get postprints archiving permissions
            for value in root.findall('publishers/publisher'):
                poa=value.find('preprints/postarchiving')
                if poa is None:pass
                else:
                    poaText=poa.text
                    row['Postarchiving_permissions'] = poaText

            #get postprints archiving restrictions
            for value in root.findall('publishers/publisher'):
                por=value.find('postprints/prerestrictions')
                if por is None:pass
                else:
                    porText=por.text
                    row['Postarchiving_restrictions'] = porText

            # get PDF archiving permissions
            for value in root.findall('publishers/publisher'):
                pdfA=value.find('pdfversion/pdfarchiving')
                if pdfA is None:pass
                else:
                    pdfAText=pdfA.text
                    row['PDFarchiving_permissions'] = pdfAText

            #get PDF archiving restrictions
            for value in root.findall('publishers/publisher'):
                pdfR=value.find('pdfversion/pdfrestrictions')
                if pdfR is None:pass
                else:
                    pdfRText=pdfR.text
                    row['PDFarchiving_restrictions'] = pdfRText

            #get publisher conditions
            conditions=[]
            for value in root.findall('publishers/publisher/conditions'):
                cond=value.findall('condition')
                # print(cond)
                for x in cond:
                    if x is None:pass
                    else:
                        conditions.append(x.text)
                        # condText=blah.join(';')
                row['Publisher_conditions'] = "||".join(conditions)



    # # Now we've finished manipulating our data structure, we want to write it
    # # back into csv somewhere on disk. Keep in mind I added a column, so I
    # # have to specify that in the field_names array
    #
    # # make our field_names array reflect any changes in the data
    #
    # # copy our original the cheating-y way because strings are immutable
    field_names = [x for x in original_fields]
    # # add the column we added to everything
    field_names.append('NumberOfHits')
    field_names.append('Prearchiving_permissions')
    field_names.append('Prearchiving_restrictions')
    field_names.append('Postarchiving_permissions')
    field_names.append('Postarchiving_restrictions')
    field_names.append('PDFarchiving_permissions')
    field_names.append('PDFarchiving_restrictions')
    field_names.append('Publisher_conditions')

    write_list_of_dicts_to_file(outfile_path, rows, field_names)
    #
# make this a safe-ish cli script
if __name__ == '__main__':
    main()
