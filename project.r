# import data
dataInitial <- read.csv("../Desktop/imdb-movie-data.csv") # insert the proper path here

# select attributes
dataUnpartitioned = subset(dataInitial, select=c(Genre, Director, Actors, Runtime..Minutes., Rating))

# train/test data partition
smp_size <- floor(0.75 * nrow(dataUnpartitioned))
set.seed(123)
train_ind <- sample(seq_len(nrow(dataUnpartitioned)), size = smp_size)
data <- dataUnpartitioned[train_ind, ]
testData <- dataUnpartitioned[-train_ind, ]

# Then do clustering on the rating:
set.seed(20)
successCluster <- kmeans(data[, 5], 3, nstart = 20)

# initialize variables
actorList <- list()
allActors <- list()
actorScore <- list()
genreList <- list()
allGenres <- list()
genreScore <- list()
directorList <- list()
allDirectors <- list()
directorScore <- list()
  
# calculate actor score
  for (i in 1:750) {
    actors <- strsplit(as.character(data[3][i,]), ", ")
    for (j in 1:length(actors[[1]])) {
      actorIndex <- match(actors[[1]][j], allActors)
      clusterValue <- 1
      if (successCluster$cluster[[i]] == 2) {
        clusterValue <- 0.5
      } else if (successCluster$cluster[[i]] == 3) {
        clusterValue <- 0
      }
      if (is.na(actorIndex)) {
        allActors[[length(allActors) + 1]] <- actors[[1]][j]
        actorList[[length(actorList) + 1]] <- list(actors[[1]][j], list(clusterValue))
      } else {
        clusterList <- actorList[[actorIndex]][[2]]
        clusterList[[length(clusterList) + 1]] <- clusterValue
      }
    }
  }
  
  
  for (i in 1:750) {
    actors <- strsplit(as.character(data[3][i,]), ", ")
    rowClusters <- list()
    for (j in 1:length(actors[[1]])) {
      actorIndex <- match(actors[[1]][j], allActors)
      clusterList <- actorList[[actorIndex]][[2]]
      rowClusters[[length(rowClusters) + 1]] <- mean(unlist(clusterList))
    }
    actorScore[[length(actorScore) + 1]] <- mean(unlist(rowClusters))
  }
  
# calculate genreScore
  for (i in 1:750) {
    genre <- strsplit(as.character(data[1][i,]), ",")
    for (j in 1:length(genre[[1]])) {
      genreIndex <- match(genre[[1]][j], allGenres)
      clusterValue <- 1
      if (successCluster$cluster[[i]] == 2) {
        clusterValue <- 0.5
      } else if (successCluster$cluster[[i]] == 3) {
        clusterValue <- 0
      }
      if (is.na(genreIndex)) {
        allGenres[[length(allGenres) + 1]] <- genre[[1]][j]
        genreList[[length(genreList) + 1]] <- list(genre[[1]][j], list(clusterValue))
      } else {
        clusterList <- genreList[[genreIndex]][[2]]
        clusterList[[length(clusterList) + 1]] <- clusterValue
      }
    }
  }
  
  
  for (i in 1:750) {
    genres <- strsplit(as.character(data[1][i,]), ",")
    rowClusters <- list()
    for (j in 1:length(genres[[1]])) {
      genreIndex <- match(genres[[1]][j], allGenres)
      clusterList <- genreList[[genreIndex]][[2]]
      rowClusters[[length(rowClusters) + 1]] <- mean(unlist(clusterList))
    }
    genreScore[[length(genreScore) + 1]] <- mean(unlist(rowClusters))
  }
  
  
  # calculate directorScore
  for (i in 1:750) {
    director <- strsplit(as.character(data[1][i,]), ",")
    for (j in 1:length(director[[1]])) {
      directorIndex <- match(director[[1]][j], allDirectors)
      clusterValue <- 1
      if (successCluster$cluster[[i]] == 2) {
        clusterValue <- 0.5
      } else if (successCluster$cluster[[i]] == 3) {
        clusterValue <- 0
      }
      if (is.na(directorIndex)) {
        allDirectors[[length(allDirectors) + 1]] <- director[[1]][j]
        directorList[[length(directorList) + 1]] <- list(director[[1]][j], list(clusterValue))
      } else {
        clusterList <- directorList[[directorIndex]][[2]]
        clusterList[[length(clusterList) + 1]] <- clusterValue
      }
    }
  }
  
  
  for (i in 1:750) {
    directors <- strsplit(as.character(data[1][i,]), ",")
    rowClusters <- list()
    for (j in 1:length(directors[[1]])) {
      directorIndex <- match(directors[[1]][j], allDirectors)
      clusterList <- directorList[[directorIndex]][[2]]
      rowClusters[[length(rowClusters) + 1]] <- mean(unlist(clusterList))
    }
    directorScore[[length(directorScore) + 1]] <- mean(unlist(rowClusters))
  }

# change to dataframe 
dataDF <- as.data.frame(data)

# merge columns into data
  dataDF$actorScore <- as.double(actorScore)
  dataDF$genreScore <- as.double(genreScore)
  dataDF$directorScore <- as.double(directorScore)
  
  
  # perform Linear regression:
  lmRating = lm(Rating~Runtime..Minutes. + actorScore + genreScore, data = dataDF)
  summary(lmRating) # this is to see the result of the operation
  
  # predict the test data
  prediction <- predict(lmRating, newData=testData)
  prediction
  