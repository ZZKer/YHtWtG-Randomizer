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
