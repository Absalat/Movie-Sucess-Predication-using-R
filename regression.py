def regression(data, learningRate=0.0001, numOfIterations=10000):
    numOfCoefficients = len(data[0])
    coefficients = [0] * numOfCoefficients
    for i in range(numOfIterations):
        coefficients = epoch(data, learningRate, coefficients)
    return coefficients


def epoch(data, learningRate, coefficients):
    h = []
    for row in data:
        h2 = coefficients[0]
        for j in range(len(coefficients) - 1):
            coefficient = coefficients[j + 1]
            h2 += coefficient * row[j]
        h.append(h2)

    newCoefficients = []
    for i in range(len(coefficients)):
        coefficient = coefficients[i]
        summation = 0
        for j in range(len(data)):
            row = data[j]
            h2 = h[j]
            residual = h2 - row[-1]
            sumTerm = residual if i == 0 else residual * (row[i - 1])
            summation += sumTerm
        newCoefficient = coefficient - (learningRate / len(data)) * summation
        newCoefficients.append(newCoefficient)

    return newCoefficients
