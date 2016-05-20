# -- coding: utf-8 --
import csv, sys

with open(sys.argv[1], mode='rU', errors='ignore') as infile:
    with open(sys.argv[2], 'w') as resultsFile:
        writer = csv.writer(resultsFile, lineterminator='\n')
        reader = csv.DictReader(infile)
        dedupeDOI = {}
        dedupeFreq = {}
        writer.writerow(("Author", "Department", "Title", "Year_Published", "Journal", "Publisher", "Published_URL", "KUSW_URL", "Rights_to_Share", "Conditions", "SourceFile","DuplicateHandle","DuplicateDOI"))
        for row in reader:
            DOI = row['DOI']
            duplicateFlag=""
            if len(DOI) > 0:
                dedupeFreq[DOI] = dedupeFreq.get(DOI, 0) + 1
                if dedupeFreq[DOI] > 1:
                    duplicateFlag = "duplicate"
                    # print(handle, duplicateFlag)

                if not DOI.strip():
                        DOI = dedupeDOI.get(DOI, "")
            x=(row["Author"], row["Department"], row["Title"], row["Year_Published"], row["Journal"],
               row["Publisher"], row["Published_URL"], DOI, row["Rights_to_Share"], row["Conditions"], row["SourceFile"], row["DuplicateHandle"], duplicateFlag)
            writer.writerow(x)
