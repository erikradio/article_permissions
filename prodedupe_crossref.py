import csv, json
import sys
import requests


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
        "SourceFile", "DuplicateHandle", "DuplicateDOI"
        ]

    # Get our original data structure
    rows = read_file_get_list_of_dicts(infile_path)
    original_fields = [x for x in rows[0].keys()]

    # Manipulate that structure however we want, in this case I add another
    # column to everything called "brian_column" that has a random uuid in it
    crossref_url = 'http://api.crossref.org/works/'

    # Set a counter to print so we know how fast things are going
    i = 0
    m = len(rows)

    for row in rows:

        # increment our counter
        i += 1
        # print the counter
        print("{}/{}".format(str(i), str(m)))

        DOI = row['DOI']
        if len(DOI) > 0:
            req = requests.get(crossref_url+DOI)

            # if req.status_code == '404':pass
            if req.status_code == requests.codes.ok:

                req = req.json()

                try:
                    title = req['message']['title'][0]
                except (KeyError, IndexError):
                    title = ""

                try:
                    issn = req['message']['ISSN'][0]
                except (KeyError, IndexError):
                    issn = ""

                try:
                    journal_title = req['message']['container-title'][0]
                except (KeyError, IndexError):
                    journal_title = ""

                try:
                    authors =req['message']['author']
                except KeyError:
                    authors = []



                # We need to do fancy stuff with author names
                # Start an array we'll be filling with str entries
                # formatted as "last, first"
                auth_names = []

                for author in authors:
                    # Put both names in a list
                    try:
                        auth_name_list = [author['family'], author['given']]
                    except KeyError:
                        auth_name_list=[]
                    # print(auth_name_list)
                    # Throw a comma and a space in between them
                    auth_name = ", ".join(auth_name_list)
                    # Add them to our list of "last, first" strs
                    auth_names.append(auth_name)


                # Take every entry in our list of "last, first" strs and jam them
                # together into one big string separated by the double pipe
                # characters.

                row['Crossref_author'] = "||".join(auth_names)
                row['Crossref_title'] = title
                row['Crossref_issn'] = issn
                row['Crossref_journal'] = journal_title

    # Now we've finished manipulating our data structure, we want to write it
    # back into csv somewhere on disk. Keep in mind I added a column, so I
    # have to specify that in the field_names array

    # make our field_names array reflect any changes in the data

    # copy our original the cheating-y way because strings are immutable
    field_names = [x for x in original_fields]
    # add the column we added to everything
    field_names.append('Crossref_author')
    field_names.append('Crossref_title')
    field_names.append('Crossref_journal')
    field_names.append('Crossref_author')
    field_names.append('Crossref_issn')

    write_list_of_dicts_to_file(outfile_path, rows, field_names)

# make this a safe-ish cli script
if __name__ == '__main__':
    main()
