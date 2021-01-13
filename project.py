import csv
from clustering import kmeans
from regression import regression

def readCsv(filename):
    myCsv = []
    with open(filename) as file:
        csv_reader = csv.reader(file)
        line_count = 0
        for row in csv_reader:
            myCsv.append(row)
    return myCsv


def selectAttributes(myCsv):
    for i in range(len(myCsv)):
        oldRow = myCsv[i]
        newRow = []
        newRow.append(oldRow[2])
        newRow.append(oldRow[4])
        newRow.append(oldRow[5])
        newRow.append(oldRow[6])
        newRow.append(oldRow[7])
        newRow.append(oldRow[11])
        myCsv[i] = newRow

def classifyTrainTest(myCsv):
    trainPercentage = 0.8
    testStartIndex = int(trainPercentage * (len(myCsv) - 1) + 1)
    data = myCsv[1:testStartIndex]
    testData = myCsv[testStartIndex:len(myCsv)]
    return data, testData

def getClusters(data):
    attendance = [row[5] for row in data]
    centroids, clusters = kmeans([int(i) for i in attendance], 3)
    hitCentroidIndex = centroids.index(max(centroids))
    flopCentroidIndex = centroids.index(min(centroids))
    newClusters = []
    for cluster in clusters:
        newClusterIndex = 0
        if cluster == hitCentroidIndex:
            newClusterIndex = 2
        elif cluster == flopCentroidIndex:
            newClusterIndex = 0
        else:
            averageCentroidIndex = cluster
            newClusterIndex = 1
        newClusters.append(newClusterIndex)
    newCentroids = [0, 0, 0]
    newCentroids[0] = min(centroids)
    newCentroids[1] = centroids[averageCentroidIndex]
    newCentroids[2] = max(centroids)
    return newCentroids, newClusters

def getScores(data, clusters, column, delimeter):
    scores = []
    actorScore = []
    allActors = []
    for i in range(len(data)):
        row = data[i]
        actors = row[column].split(delimeter)
        for actor in actors:
            if clusters[i] == 0:
                clusterValue = 0
            elif clusters[i] == 1:
                clusterValue = 0.5
            else:
                clusterValue = 1
                
            if actor in allActors:
                actorScore[allActors.index(actor)][1].append(clusterValue)
            else:
                allActors.append(actor)
                actorScore.append([actor, [clusterValue]])

    for i in range(len(data)):
        row = data[i]
        actors = row[column].split(delimeter)
        score = 0
        for actor in actors:
            index = allActors.index(actor)
            actorScoreList = actorScore[index][1]
            score += sum(actorScoreList) / len(actorScoreList)
        score /= len(actors)
        scores.append(score)
    return scores

def getActorScores(data, clusters):
    return getScores(data, clusters, 2, ", ")

def getGenreScores(data, clusters):
    return getScores(data, clusters, 0, ",")

def getDirectorScores(data, clusters):
    return getScores(data, clusters, 1, ", ")

def mergeColumnsIntoData(data, columns):
    mergedData = data[:]
    for i in range(len(mergedData)):
        row = mergedData[i]
        for column in columns:
            mergedData[i].append(column[i])
    return mergedData

def prepareForRegression(data):
    newData = []
    for i in range(len(data)):
        row = data[i]
        newData.append([row[6], row[7], row[8], int(row[3]), float(row[4]), int(row[5])])
    return newData

def printRegressionResult(coefficients):
    x0 = str(round(coefficients[0], 1))
    x1 = str(round(coefficients[1], 1))
    x2 = str(round(coefficients[2], 1))
    x3 = str(round(coefficients[3], 1))
    x4 = str(round(coefficients[4], 1))
    x5 = str(round(coefficients[5], 1))
    print("The linear regression equation is:")
    print("h(X) = " + x0 + " + " + x1 + "X1 + " + x2 + "X2 + " + x3 + "X3 + " + x4 + "X4 + " + x5 + "X5")
    print("\nWhere:")
    print("h(X) is the predicted attendance,")
    print("X1 is the actorScore,")
    print("X2 is the genreScore,")
    print("X3 is the directorScore,")
    print("X4 is the running time in minutes, and")
    print("X5 is the rating.")

def calculateTestCluster(attendance, centroids):
    distances = []
    for centroid in centroids:
        distances.append(abs(centroid - attendance))
    shortest = min(distances)
    index = distances.index(shortest)
    return index

def testEquation(testData, coefficients, centroids):
    centroids, clusters = getClusters(testData)
    actorScores = getActorScores(testData, clusters)
    genreScores = getGenreScores(testData, clusters)
    directorScores = getDirectorScores(testData, clusters)
    mergedData = mergeColumnsIntoData(testData, [actorScores, genreScores, directorScores])
    predictedClusters = []
    for i in range(len(mergedData)):
        row = mergedData[i]
        attendance = coefficients[0] + coefficients[1] * row[6] + coefficients[2] * row[7] + coefficients[3] * row[8]\
                     + coefficients[4] * int(row[3]) + coefficients[5] * float(row[4])
        predictedCluster = calculateTestCluster(attendance, centroids)
        predictedClusters.append(predictedCluster)

    # test accuracy
    _, testClusters = getClusters(testData)
    accurateCount = 0
    for i in range(len(testClusters)):
        if predictedClusters[i] == testClusters[i]:
            accurateCount += 1
    return accurateCount
        
def main():
    myCsv = readCsv("imdb-movie-data.csv")
    selectAttributes(myCsv)
    data, testData = classifyTrainTest(myCsv)
    centroids, clusters = getClusters(data)
    actorScores = getActorScores(data, clusters)
    genreScores = getGenreScores(data, clusters)
    directorScores = getDirectorScores(data, clusters)
    mergedData = mergeColumnsIntoData(data, [actorScores, genreScores, directorScores])
    regressionReadyData = prepareForRegression(mergedData)
    coefficients = regression(regressionReadyData)
    printRegressionResult(coefficients)
    accurateCount = testEquation(testData, coefficients, centroids)
    print("\n________________________________________\n")
    print(accurateCount, "of", len(testData), "test data predicted accurately giving an overall accuracy of", round(accurateCount / len(testData), 2))

main()
