# -- coding: utf-8 --
import csv, sys

with open(sys.argv[1], mode='rU', errors='ignore') as infile:
    with open(sys.argv[2], 'w') as resultsFile:
        writer = csv.writer(resultsFile, lineterminator='\n')
        reader = csv.DictReader(infile)
        dedupeHandles = {}
        dedupeFreq = {}
        writer.writerow(("Author", "Department", "Title", "Year_Published","DOI", "Journal", "Publisher", "Published_URL", "KUSW_URL", "Rights_to_Share", "Conditions", "SourceFile","DuplicateHandle"))
        for row in reader:
            handle = row['KUSW_URL']
            duplicateFlag=""
            if len(handle) > 0:
                dedupeFreq[handle] = dedupeFreq.get(handle, 0) + 1
                if dedupeFreq[handle] > 1:
                    duplicateFlag = "duplicate"
                    # print(handle, duplicateFlag)

                if not handle.strip():
                        handle = dedupeHandles.get(handle, "")
            x=(row["Author"], row["Department"], row["Title"], row["Year_Published"],row["DOI"], row["Journal"],
               row["Publisher"], row["Published_URL"], handle, row["Rights_to_Share"], row["Conditions"], row["SourceFile"], duplicateFlag)
            writer.writerow(x)
