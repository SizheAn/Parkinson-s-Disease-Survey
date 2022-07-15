import csv
import codecs
import difflib as df


keywordFilter = ["parkinson","parkinson's disease", "bradykinesia", "dyskinesia", "tremor", "on-off", "on-off states", "PRKN", "levodopa", "fog", "freezing of gait", "L-DOPA"]

technologyFilter = ["acceleration","accelerometer","gyroscope","magnetometer", "gyro","acc","exoskeleton device", "inertial sensor","inertial","video recording","video camera","camera","ehealth",
                    "wearable technology","wearable accelerometer", "technology", "remote monitoring","home monitoring","telemedicine","mobile phone", "mobile application", "precision medicine",
                    "digital health","accelerometer", "gyroscope", "imu", "wearable", "wearable sensor","biosensor", "magneto inertial sensor","wearable inertial sensors", "sensor", "smartphone",
                    "augmented reality","kinect","ecg", "eeg", "emg", "eog", "meg", "electrocardiography", "electroencephalography", "electromyography", "electrooculography", "magnetoencephalography",
                    "machine learning", "classification", "auditory cue","auditory cueing", "gait classification", "bayesian network","naive vayes", "random forest", "insole sensors", "leap motion",
                    "computer vision", "supervised learning","neural networks", "deep learning", "speech disorder", "music therapy", "smart application", "smartphone application", "insole sensor",
                    "smart watch", "fitness band"]
ignoreList = ["mice", "mouse", "rat", "rats", "animal", "primates", "marmoset", "monkey", "monkeys"]
technologyIgnore = ["MRI", "fmri", "magnetic resonance imaging", "magnetic resonance images", "SPECT", "PET", "Positron emission tomography", "Single-photon emission computed tomography",
                    "Deep Brain Stimulation", "DBS" ,"Transcranial", "neuroimaging", "brain imaging"]


key = set()

keywordCount = {}

newResults = []
techIgnore = []
animalIgnore = []
rejected = []

tot = 0
ktot = 0
ntot = 0
with codecs.open('sd_2020_21_english.csv', 'r', encoding='ISO-8859-1') as csvfile:
    filereader = csv.reader(csvfile, delimiter = ',',
                                quotechar = '"')
    h = next(filereader, None)
    for row in filereader:
        print(row[0])
        tot = tot+1
        if row[6] == "":
            rejected.append(row)
            continue
        keywords = row[6].split(",")
        match = False
        abstractKeys = []
        abstract = row[5].lower().replace('&rsquo;', "'")
        title = row[0]
        #id = row[15]
        #if id == '10.3233/JPD-2012-12077':
        #    n = 10
            # text = html.unescape(row[6])
        # if title == 'A Validation Study of Freezing of Gait (FoG) Detection and Machine-Learning-Based FoG Prediction Using Estimated Gait Characteristics with a Wearable Accelerometer':
        #    n = 10
        ignore = False
        for k in keywords:
            match = df.get_close_matches(k.lower(), ignoreList, n=1, cutoff=0.9)
            if len(match) != 0:
                ignore = True
                row.append('Keywords ' + k)
                animalIgnore.append(row)
                break
        if ignore == True:
            continue
        for t in ignoreList:
            if ' ' + t + ' ' in abstract or ' ' + t + ',' in abstract or ' ' + t + '.' in abstract or ' ' + t + ';' in abstract or ' ' + t + '-' in abstract \
                    or ' ' + t + 's ' in abstract or ' ' + t + 's,' in abstract or ' ' + t + 's.' in abstract or ' ' + t + 's;' in abstract or ' ' + t + 's-' in abstract:
                ignore = True
                row.append('Abstract ' + t)
                animalIgnore.append(row)
                break
        if ignore == True:
            continue

        for k in keywords:
            match = df.get_close_matches(k.lower(), technologyIgnore, n=1, cutoff=0.9)
            if len(match) != 0:
                row.append('Keywords ' + k)
                techIgnore.append(row)
                ignore = True
                break

        if ignore == True:
            continue

        for t in technologyIgnore:
            if ' ' + t + ' ' in abstract or ' ' + t + ',' in abstract or ' ' + t + '.' in abstract or ' ' + t + ';' in abstract or ' ' + t + '-' in abstract \
                    or ' ' + t + 's ' in abstract or ' ' + t + 's,' in abstract or ' ' + t + 's.' in abstract or ' ' + t + 's;' in abstract or ' ' + t + 's-' in abstract:
                ignore = True
                row.append('Abstract ' + t)
                techIgnore.append(row)
                break

        if ignore == True:
            continue

        if row[0] == 'Detection of inflammatory biomarkers in saliva and urine: Potential in diagnosis, prevention, and treatment for chronic diseases':
            print("problem")
        park = False
        for k in keywords:
            matches = df.get_close_matches(k.lower(), keywordFilter, n=1, cutoff=0.9)
            if len(matches) != 0:
                park = True
                break

        if park != True:
            parkAbs = []
            for t in keywordFilter:
                if ' ' + t + ' ' in abstract or ' ' + t + ',' in abstract or ' ' + t + '.' in abstract or ' ' + t + ';' in abstract or ' ' + t + '-' in abstract \
                        or ' ' + t + 's ' in abstract or ' ' + t + 's,' in abstract or ' ' + t + 's.' in abstract or ' ' + t + 's;' in abstract or ' ' + t + 's-' in abstract:
                    parkAbs.append(t)
            if len(parkAbs) != 0:
                park = True



        for t in keywords:
            tech = df.get_close_matches(t.lower(), technologyFilter, n=1, cutoff=0.9)
            if len(tech) != 0:
                match = True
                if t == 'Health':
                    print("health")
                row.append('Keywords ' + t)
                break
            else:
                parts = t.split(' ')
                for w in parts:
                    tech = df.get_close_matches(w.lower(), technologyFilter, n=1, cutoff=0.9)
                    if len(tech) != 0:
                        if w == 'Health':
                            print("health")
                        row.append('Keywords ' + w)
                        match = True
                        break

            # exist = df.get_close_matches(t.lower(), keys, n=1, cutoff=0.9)
            # if len(exist) != 0:
            #     print(keywordCount[exist[0]])
            #     keywordCount[exist[0]] = keywordCount[exist[0]]+1
            # else:
            #     keywordCount[t] = 1
            if match == True:
                break;
        # abstract = row[6]

        if park == True:
            for t in technologyFilter:
                if ' ' + t + ' ' in abstract or ' ' + t + ',' in abstract or ' ' + t + '.' in abstract or ' ' + t + ';' in abstract or ' ' + t + '-' in abstract \
                        or ' ' + t + 's ' in abstract or ' ' + t + 's,' in abstract or ' ' + t + 's.' in abstract or ' ' + t + 's;' in abstract or ' ' + t + 's-' in abstract:
                    abstractKeys.append(t)
            if len(abstractKeys) != 0:
                if match == True:
                    s = row[-1]
                    s = s + ' ' + 'Abstract ' + ', '.join(abstractKeys)
                    row[-1] = s
                else:
                    row.append('Abstract ' + ', '.join(abstractKeys))
                    match = True

        if match == True:
            newResults.append(row)
            keys = keywordCount.keys()
            totalKeys = row[6].split(",")
            for m in abstractKeys:
                if m not in totalKeys:
                    totalKeys.append(m)
            # totalKeys.append(abstractKeys)
            for i in totalKeys:
                exist = df.get_close_matches(i.lower(), technologyFilter, n=1, cutoff=0.9)
                if len(exist) != 0:
                    if exist[0] in keywordCount.keys():
                        print(keywordCount[exist[0]])
                        keywordCount[exist[0]] = keywordCount[exist[0]] + 1
                    else:
                        keywordCount[exist[0]] = 1
            continue

        else:
            rejected.append(row)


print("FIn")

with codecs.open('SDprocessedNew062422.csv', 'w', encoding='utf8') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
    filewriter.writerow(['Title', 'Authors', 'Published in', 'Year', 'Document Type', 'Keywords', 'Abstract', 'Identifier','Reason'])
    csvfile.flush()

    for line in newResults:
        pack = line[:8]
        pack.append(line[-1])
        filewriter.writerow(pack)
        csvfile.flush()



with codecs.open('PMC_E_full06222022.csv', 'r', encoding='utf8') as csvfile:
    filereader = csv.reader(csvfile, delimiter = ',',
                                quotechar = '"')
    h = next(filereader, None)
    for row in filereader:
        # print(','.join(row))
        tot = tot + 1
        if row[5] == "":
            rejected.append(row)
            continue
        keywords = row[5].split(",")
        match = False
        abstractKeys = []
        abstract = row[6].lower().replace('&rsquo;', "'")
        title = row[0]
        id = row[7]
        if id == '10.3233/JPD-2012-12077':
            n = 10
        if title == 'Towards an Automated Unsupervised Mobility Assessment for Older People Based on Inertial TUG Measurements':
            n = 10
            # text = html.unescape(row[6])
        # if title == 'A Validation Study of Freezing of Gait (FoG) Detection and Machine-Learning-Based FoG Prediction Using Estimated Gait Characteristics with a Wearable Accelerometer':
        #    n = 10
        ignore = False
        for k in keywords:
            match = df.get_close_matches(k.lower(), ignoreList, n=1, cutoff=0.9)
            if len(match) != 0:
                ignore = True
                row.append('Keywords ' + k)
                animalIgnore.append(row)
                break
        if ignore == True:
            continue
        for t in ignoreList:
            if ' ' + t + ' ' in abstract or ' ' + t + ',' in abstract or ' ' + t + '.' in abstract or ' ' + t + ';' in abstract or ' ' + t + '-' in abstract \
                    or ' ' + t + 's ' in abstract or ' ' + t + 's,' in abstract or ' ' + t + 's.' in abstract or ' ' + t + 's;' in abstract or ' ' + t + 's-' in abstract:
                ignore = True
                row.append('Abstract ' + t)
                animalIgnore.append(row)
                break
        if ignore == True:
            continue

        for k in keywords:
            match = df.get_close_matches(k.lower(), technologyIgnore, n=1, cutoff=0.9)
            if len(match) != 0:
                row.append('Keywords ' + k)
                techIgnore.append(row)
                ignore = True
                break

        if ignore == True:
            continue

        for t in technologyIgnore:
            if ' ' + t + ' ' in abstract or ' ' + t + ',' in abstract or ' ' + t + '.' in abstract or ' ' + t + ';' in abstract or ' ' + t + '-' in abstract \
                    or ' ' + t + 's ' in abstract or ' ' + t + 's,' in abstract or ' ' + t + 's.' in abstract or ' ' + t + 's;' in abstract or ' ' + t + 's-' in abstract:
                ignore = True
                row.append('Abstract ' + t)
                techIgnore.append(row)
                break
        if ignore == True:
            continue

        if row[
            0] == 'Detection of inflammatory biomarkers in saliva and urine: Potential in diagnosis, prevention, and treatment for chronic diseases':
            print("problem")
        park = False
        for k in keywords:
            # words = k.split(' ')
            # for w in words:
            matches = df.get_close_matches(k.lower(), keywordFilter, n=1, cutoff=0.9)
            if len(matches) != 0:
                park = True
                break

        if park != True:
            parkAbs = []
            for t in keywordFilter:
                if ' ' + t + ' ' in abstract or ' ' + t + ',' in abstract or ' ' + t + '.' in abstract or ' ' + t + ';' in abstract or ' ' + t + '-' in abstract \
                        or ' ' + t + 's ' in abstract or ' ' + t + 's,' in abstract or ' ' + t + 's.' in abstract or ' ' + t + 's;' in abstract or ' ' + t + 's-' in abstract:
                    parkAbs.append(t)
            if len(parkAbs) != 0:
                # row.append('Abstract ' + ', '.join(abstractKeys))
                park = True

        for t in keywords:
            tech = df.get_close_matches(t.lower(), technologyFilter, n=1, cutoff=0.9)
            if len(tech) != 0:
                match = True
                if t == 'Health':
                    print("health")
                row.append('Keywords ' + t)
                break
            else:
                parts = t.split(' ')
                for w in parts:
                    tech = df.get_close_matches(w.lower(), technologyFilter, n=1, cutoff=0.9)
                    if len(tech) != 0:
                        if w == 'Health':
                            print("health")
                        row.append('Keywords ' + w)
                        match = True
                        break

            # exist = df.get_close_matches(t.lower(), keys, n=1, cutoff=0.9)
            # if len(exist) != 0:
            #     print(keywordCount[exist[0]])
            #     keywordCount[exist[0]] = keywordCount[exist[0]]+1
            # else:
            #     keywordCount[t] = 1
            if match == True:
                break;
        # abstract = row[6]

        if park == True:
            for t in technologyFilter:
                if ' ' + t + ' ' in abstract or ' ' + t + ',' in abstract or ' ' + t + '.' in abstract or ' ' + t + ';' in abstract or ' ' + t + '-' in abstract \
                        or ' ' + t + 's ' in abstract or ' ' + t + 's,' in abstract or ' ' + t + 's.' in abstract or ' ' + t + 's;' in abstract or ' ' + t + 's-' in abstract:
                    abstractKeys.append(t)
            if len(abstractKeys) != 0:
                if match == True:
                    s = row[-1]
                    s = s + ' ' + 'Abstract ' + ', '.join(abstractKeys)
                    row[-1] = s
                else:
                    row.append('Abstract ' + ', '.join(abstractKeys))
                    match = True

        if match == True:
            newResults.append(row)
            keys = keywordCount.keys()
            totalKeys = row[5].split(",")
            for m in abstractKeys:
                if m not in totalKeys:
                    totalKeys.append(m)
            # totalKeys.append(abstractKeys)
            for i in totalKeys:
                exist = df.get_close_matches(i.lower(), technologyFilter, n=1, cutoff=0.9)
                if len(exist) != 0:
                    if exist[0] in keywordCount.keys():
                        print(keywordCount[exist[0]])
                        keywordCount[exist[0]] = keywordCount[exist[0]] + 1
                    else:
                        keywordCount[exist[0]] = 1
            continue

        else:
            rejected.append(row)

print("FIn")


with codecs.open('PMCprocessedNew062422.csv', 'w', encoding='utf8') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
    filewriter.writerow(['Title', 'Authors', 'Published in', 'Year', 'Document Type', 'Keywords', 'Abstract', 'Identifier','Reason'])
    csvfile.flush()

    for line in newResults:
        pack = line[:8]
        pack.append(line[-1])
        filewriter.writerow(pack)
        csvfile.flush()




with codecs.open('ieee2020_21.csv', 'r', encoding='utf8') as csvfile:
    filereader = csv.reader(csvfile, delimiter = ',',
                                quotechar = '"')
    h = next(filereader, None)
    for row in filereader:
        # print(','.join(row))
        tot = tot + 1
        if row[5] == "":
            rejected.append(row)
            continue
        keywords = row[5].split(";")
        match = False
        abstractKeys = []
        abstract = row[6].lower().replace('&rsquo;', "'")
        title = row[0]
        if title == 'Towards an Automated Unsupervised Mobility Assessment for Older People Based on Inertial TUG Measurements':
            n = 10
            # text = html.unescape(row[6])
        # if title == 'A Validation Study of Freezing of Gait (FoG) Detection and Machine-Learning-Based FoG Prediction Using Estimated Gait Characteristics with a Wearable Accelerometer':
        #    n = 10
        ignore = False
        for k in keywords:
            match = df.get_close_matches(k.lower(), ignoreList, n=1, cutoff=0.9)
            if len(match) != 0:
                ignore = True
                row.append('Keywords ' + k)
                animalIgnore.append(row)
                break
        if ignore == True:
            continue
        for t in ignoreList:
            if ' ' + t + ' ' in abstract or ' ' + t + ',' in abstract or ' ' + t + '.' in abstract or ' ' + t + ';' in abstract or ' ' + t + '-' in abstract \
                    or ' ' + t + 's ' in abstract or ' ' + t + 's,' in abstract or ' ' + t + 's.' in abstract or ' ' + t + 's;' in abstract or ' ' + t + 's-' in abstract:
                ignore = True
                row.append('Abstract ' + t)
                animalIgnore.append(row)
                break
        if ignore == True:
            continue

        for k in keywords:
            match = df.get_close_matches(k.lower(), technologyIgnore, n=1, cutoff=0.9)
            if len(match) != 0:
                row.append('Keywords ' + k)
                techIgnore.append(row)
                ignore = True
                break

        if ignore == True:
            continue

        for t in technologyIgnore:
            if ' ' + t + ' ' in abstract or ' ' + t + ',' in abstract or ' ' + t + '.' in abstract or ' ' + t + ';' in abstract or ' ' + t + '-' in abstract \
                    or ' ' + t + 's ' in abstract or ' ' + t + 's,' in abstract or ' ' + t + 's.' in abstract or ' ' + t + 's;' in abstract or ' ' + t + 's-' in abstract:
                ignore = True
                row.append('Abstract ' + t)
                techIgnore.append(row)
                break
        if ignore == True:
            continue

        if row[
            0] == 'Detection of inflammatory biomarkers in saliva and urine: Potential in diagnosis, prevention, and treatment for chronic diseases':
            print("problem")
        park = False
        for k in keywords:
            # words = k.split(' ')
            # for w in words:
            matches = df.get_close_matches(k.lower(), keywordFilter, n=1, cutoff=0.9)
            if len(matches) != 0:
                park = True
                break

        if park != True:
            parkAbs = []
            for t in keywordFilter:
                if ' ' + t + ' ' in abstract or ' ' + t + ',' in abstract or ' ' + t + '.' in abstract or ' ' + t + ';' in abstract or ' ' + t + '-' in abstract \
                        or ' ' + t + 's ' in abstract or ' ' + t + 's,' in abstract or ' ' + t + 's.' in abstract or ' ' + t + 's;' in abstract or ' ' + t + 's-' in abstract:
                    parkAbs.append(t)
            if len(parkAbs) != 0:
                # row.append('Abstract ' + ', '.join(abstractKeys))
                park = True

        for t in keywords:
            tech = df.get_close_matches(t.lower(), technologyFilter, n=1, cutoff=0.9)
            if len(tech) != 0:
                match = True
                if t == 'Health':
                    print("health")
                row.append('Keywords ' + t)
                break
            else:
                parts = t.split(' ')
                for w in parts:
                    tech = df.get_close_matches(w.lower(), technologyFilter, n=1, cutoff=0.9)
                    if len(tech) != 0:
                        if w == 'Health':
                            print("health")
                        row.append('Keywords ' + w)
                        match = True
                        break

            # exist = df.get_close_matches(t.lower(), keys, n=1, cutoff=0.9)
            # if len(exist) != 0:
            #     print(keywordCount[exist[0]])
            #     keywordCount[exist[0]] = keywordCount[exist[0]]+1
            # else:
            #     keywordCount[t] = 1
            if match == True:
                break;
        # abstract = row[6]

        if park == True:
            for t in technologyFilter:
                if ' ' + t + ' ' in abstract or ' ' + t + ',' in abstract or ' ' + t + '.' in abstract or ' ' + t + ';' in abstract or ' ' + t + '-' in abstract \
                        or ' ' + t + 's ' in abstract or ' ' + t + 's,' in abstract or ' ' + t + 's.' in abstract or ' ' + t + 's;' in abstract or ' ' + t + 's-' in abstract:
                    abstractKeys.append(t)
            if len(abstractKeys) != 0:
                if match == True:
                    s = row[-1]
                    s = s + ' ' + 'Abstract ' + ', '.join(abstractKeys)
                    row[-1] = s
                else:
                    row.append('Abstract ' + ', '.join(abstractKeys))
                    match = True

        if match == True:
            newResults.append(row)
            keys = keywordCount.keys()
            totalKeys = row[5].split(",")
            for m in abstractKeys:
                if m not in totalKeys:
                    totalKeys.append(m)
            # totalKeys.append(abstractKeys)
            for i in totalKeys:
                exist = df.get_close_matches(i.lower(), technologyFilter, n=1, cutoff=0.9)
                if len(exist) != 0:
                    if exist[0] in keywordCount.keys():
                        print(keywordCount[exist[0]])
                        keywordCount[exist[0]] = keywordCount[exist[0]] + 1
                    else:
                        keywordCount[exist[0]] = 1
            continue

        else:
            rejected.append(row)

print("FIn")


with codecs.open('IEEEprocessedNew062422.csv', 'w', encoding='utf8') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
    filewriter.writerow(['Title', 'Authors', 'Published in', 'Year', 'Document Type', 'Keywords', 'Abstract', 'Identifier','Reason'])
    csvfile.flush()

    for line in newResults:
        pack = line[:8]
        pack.append(line[-1])
        filewriter.writerow(pack)
        csvfile.flush()




with codecs.open('mdpi_processed_2020_21.csv', 'r', encoding='utf8') as csvfile:
    filereader = csv.reader(csvfile, delimiter = ',',
                                quotechar = '"')
    h = next(filereader, None)
    for row in filereader:
        # print(','.join(row))
        tot = tot + 1
        if row[5] == "":
            rejected.append(row)
            continue
        keywords = row[5].split(",")
        match = False
        abstractKeys = []
        abstract = row[6].lower().replace('&rsquo;', "'")
        title = row[0]
        if title == 'Towards an Automated Unsupervised Mobility Assessment for Older People Based on Inertial TUG Measurements':
            n = 10
            # text = html.unescape(row[6])
        # if title == 'A Validation Study of Freezing of Gait (FoG) Detection and Machine-Learning-Based FoG Prediction Using Estimated Gait Characteristics with a Wearable Accelerometer':
        #    n = 10
        ignore = False
        for k in keywords:
            match = df.get_close_matches(k.lower(), ignoreList, n=1, cutoff=0.9)
            if len(match) != 0:
                ignore = True
                row.append('Keywords ' + k)
                animalIgnore.append(row)
                break
        if ignore == True:
            continue
        for t in ignoreList:
            if ' ' + t + ' ' in abstract or ' ' + t + ',' in abstract or ' ' + t + '.' in abstract or ' ' + t + ';' in abstract or ' ' + t + '-' in abstract \
                    or ' ' + t + 's ' in abstract or ' ' + t + 's,' in abstract or ' ' + t + 's.' in abstract or ' ' + t + 's;' in abstract or ' ' + t + 's-' in abstract:
                ignore = True
                row.append('Abstract ' + t)
                animalIgnore.append(row)
                break
        if ignore == True:
            continue

        for k in keywords:
            match = df.get_close_matches(k.lower(), technologyIgnore, n=1, cutoff=0.9)
            if len(match) != 0:
                row.append('Keywords ' + k)
                techIgnore.append(row)
                ignore = True
                break

        if ignore == True:
            continue

        for t in technologyIgnore:
            if ' ' + t + ' ' in abstract or ' ' + t + ',' in abstract or ' ' + t + '.' in abstract or ' ' + t + ';' in abstract or ' ' + t + '-' in abstract \
                    or ' ' + t + 's ' in abstract or ' ' + t + 's,' in abstract or ' ' + t + 's.' in abstract or ' ' + t + 's;' in abstract or ' ' + t + 's-' in abstract:
                ignore = True
                row.append('Abstract ' + t)
                techIgnore.append(row)
                break
        if ignore == True:
            continue

        if row[
            0] == 'Detection of inflammatory biomarkers in saliva and urine: Potential in diagnosis, prevention, and treatment for chronic diseases':
            print("problem")
        park = False
        for k in keywords:
            # words = k.split(' ')
            # for w in words:
            matches = df.get_close_matches(k.lower(), keywordFilter, n=1, cutoff=0.9)
            if len(matches) != 0:
                park = True
                break

        if park != True:
            parkAbs = []
            for t in keywordFilter:
                if ' ' + t + ' ' in abstract or ' ' + t + ',' in abstract or ' ' + t + '.' in abstract or ' ' + t + ';' in abstract or ' ' + t + '-' in abstract \
                        or ' ' + t + 's ' in abstract or ' ' + t + 's,' in abstract or ' ' + t + 's.' in abstract or ' ' + t + 's;' in abstract or ' ' + t + 's-' in abstract:
                    parkAbs.append(t)
            if len(parkAbs) != 0:
                # row.append('Abstract ' + ', '.join(abstractKeys))
                park = True

        for t in keywords:
            tech = df.get_close_matches(t.lower(), technologyFilter, n=1, cutoff=0.9)
            if len(tech) != 0:
                match = True
                if t == 'Health':
                    print("health")
                row.append('Keywords ' + t)
                break
            else:
                parts = t.split(' ')
                for w in parts:
                    tech = df.get_close_matches(w.lower(), technologyFilter, n=1, cutoff=0.9)
                    if len(tech) != 0:
                        if w == 'Health':
                            print("health")
                        row.append('Keywords ' + w)
                        match = True
                        break

            # exist = df.get_close_matches(t.lower(), keys, n=1, cutoff=0.9)
            # if len(exist) != 0:
            #     print(keywordCount[exist[0]])
            #     keywordCount[exist[0]] = keywordCount[exist[0]]+1
            # else:
            #     keywordCount[t] = 1
            if match == True:
                break;
        # abstract = row[6]

        if park == True:
            for t in technologyFilter:
                if ' ' + t + ' ' in abstract or ' ' + t + ',' in abstract or ' ' + t + '.' in abstract or ' ' + t + ';' in abstract or ' ' + t + '-' in abstract \
                        or ' ' + t + 's ' in abstract or ' ' + t + 's,' in abstract or ' ' + t + 's.' in abstract or ' ' + t + 's;' in abstract or ' ' + t + 's-' in abstract:
                    abstractKeys.append(t)
            if len(abstractKeys) != 0:
                if match == True:
                    s = row[-1]
                    s = s + ' ' + 'Abstract ' + ', '.join(abstractKeys)
                    row[-1] = s
                else:
                    row.append('Abstract ' + ', '.join(abstractKeys))
                    match = True

        if match == True:
            newResults.append(row)
            keys = keywordCount.keys()
            totalKeys = row[5].split(",")
            for m in abstractKeys:
                if m not in totalKeys:
                    totalKeys.append(m)
            # totalKeys.append(abstractKeys)
            for i in totalKeys:
                exist = df.get_close_matches(i.lower(), technologyFilter, n=1, cutoff=0.9)
                if len(exist) != 0:
                    if exist[0] in keywordCount.keys():
                        print(keywordCount[exist[0]])
                        keywordCount[exist[0]] = keywordCount[exist[0]] + 1
                    else:
                        keywordCount[exist[0]] = 1
            continue

        else:
            rejected.append(row)



print("FIn")

with codecs.open('MDPIprocessedNew062422.csv', 'w', encoding='utf8') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
    filewriter.writerow(['Title', 'Authors', 'Published in', 'Year', 'Document Type', 'Keywords', 'Abstract', 'Identifier', 'Reason'])
    csvfile.flush()

    for line in newResults:
        pack = line[:8]
        pack.append(line[-1])
        filewriter.writerow(pack)
        csvfile.flush()


with codecs.open('TechIgnores062422.csv', 'w', encoding='utf8') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
    filewriter.writerow(['Title', 'Authors', 'Published in', 'Year', 'Document Type', 'Keywords', 'Abstract', 'Identifier', 'Reason'])
    csvfile.flush()

    for line in techIgnore:
        pack = line[:8]
        pack.append(line[-1])
        filewriter.writerow(pack)
        csvfile.flush()

with codecs.open('NonHumanIgnores062422.csv', 'w', encoding='utf8') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
    filewriter.writerow(['Title', 'Authors', 'Published in', 'Year', 'Document Type', 'Keywords', 'Abstract', 'Identifier', 'Reason'])
    csvfile.flush()

    for line in animalIgnore:
        pack = line[:8]
        pack.append(line[-1])
        filewriter.writerow(pack)
        csvfile.flush()

with codecs.open('Rejected062422.csv', 'w', encoding='utf8') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
    filewriter.writerow(['Title', 'Authors', 'Published in', 'Year', 'Document Type', 'Keywords', 'Abstract', 'Identifier'])
    csvfile.flush()

    for line in rejected:
        pack = line[:8]
        filewriter.writerow(pack)
        csvfile.flush()
