def reduceReqs(reqs):
    reducedReqs = []
    reqs.sort()
    for req in reqs:
        add = True
        for newReq in reducedReqs:
            if not newReq & ~ req:
                add = False
                break
            elif not req & ~ newReq:
                newReq = req
                add = False
                break
        if add:
            reducedReqs = reducedReqs + [req]
    return reducedReqs

def calculateTotalRequirements(newEdgeReqs, existingReqs):
    nrNewReqs = len(newEdgeReqs)
    nrOldReqs = len(existingReqs)
    totalReqs = [0]*(nrNewReqs*nrOldReqs)
    for i in range(nrNewReqs):
        for j in range(nrOldReqs):
            totalReqs[i*nrOldReqs+j] = newEdgeReqs[i] | existingReqs[j]
    return totalReqs

def iterate(matrix, stateVector):
    ret = [[] for _ in range(len(stateVector))]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            #print(f'{matrix[j][i]}, {stateVector[i]}')
            ret[i] += calculateTotalRequirements(matrix[j][i], stateVector[j])
        #print(ret[i])
        ret[i] = reduceReqs(ret[i])
    return ret

def readTable(file):
    nrRows = 0
    nrCols = 0
    with open(file) as tableFile:
        nrCols = tableFile.readline().count(";")
        for line in tableFile:
            if line.strip():
                nrRows += 1

    if nrCols != nrRows:
        print("Table has to have the same number of rows and columns")
        return []

    table = [[[] for _ in range(nrRows)] for _ in range(nrCols)]

    with open(file) as tableFile:
        tableFile.readline()
        row = 0
        for line in tableFile:
            if not line.strip():
                continue

            lineSplits = line.split(";")[1:]
            for col in range(len(lineSplits)):
                entries = lineSplits[col].split(",")
                for entry in entries:
                    if entry.strip() and int(entry) >= 0:
                        table[row][col] += [int(entry)]
            row += 1
    return table


def writeState(writeFile, states, stateNameFile):
    stateNames = []
    writeNames = False
    with open(stateNameFile) as readFile:
        firstLineSplits = readFile.readline().split(";")
        while len(firstLineSplits) > 0 and not firstLineSplits[0].strip():
            firstLineSplits = firstLineSplits[1:]
        if len(firstLineSplits) > 0 and not firstLineSplits[0].isnumeric():
            stateNames = firstLineSplits
            writeNames = True
    with open(writeFile, 'w') as writeFile:
        if writeNames:
            writeFile.write(writeTableLine(stateNames))

        writeFile.write(writeTableLine(states))


def writeTableLine(entries):
    writeLine = ""
    if len(entries) == 0:
        print("no entries to write")
        return ""

    writeLine += writeReqEntry(entries[0])
    if len(entries) > 1:
        for entry in entries[1:]:
            writeLine += ";" + writeReqEntry(entry)

    return writeLine


def writeReqEntry(entry):
    writeReq = ""
    if len(entry) == 0:
        return ""

    if isinstance(entry, str):
        return entry

    writeReq += str(entry[0])
    if len(entry) == 1:
        return writeReq

    for req in entry[1:]:
        writeReq += "," + str(req)

    return writeReq


