import csv
import codecs

with codecs.open('MDPIprocessedNew062422.csv', 'r', encoding='utf8') as csvfile:
    filereader = csv.reader(csvfile, delimiter = ',',
                                quotechar = '"')
    h = next(filereader, None)
    filtered = []
    nodoi = []
    dois = []
    for row in filereader:
        #print(','.join(row))
        try:
            if row[7] == "":
                nodoi.append(row)
                continue
        except:
            print("Exception")
        doi1 = row[7][::-1].lower()
        i =  doi1.find('/')
        doi = doi1[0:i][::-1]
        if(doi in dois):
            print(doi)
        else:
            dois.append(doi)
            newRow = row[:7]
            newRow.append(doi)
            newRow.append(row[-1])
            filtered.append(newRow)

    with codecs.open('NewFilteredFulData062422.csv', 'w', encoding='utf8') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
        filewriter.writerow(
            ['Title', 'Authors', 'Published in', 'Year', 'Document Type', 'Keywords', 'Abstract', 'Identifier', 'Reason'])
        csvfile.flush()

        for line in filtered:
            filewriter.writerow(line[:9])
            csvfile.flush()
    with codecs.open('NoDOI062422.csv', 'w', encoding='utf8') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
        filewriter.writerow(
            ['Title', 'Authors', 'Published in', 'Year', 'Document Type', 'Keywords', 'Abstract', 'Identifier', 'Reason'])
        csvfile.flush()

        for line in nodoi:
            filewriter.writerow(line[:9])
            csvfile.flush()