import csv
import json
import math
import operator


def shannonEntropy(dataset):
    countByLabels = dict()
    for example in dataset:
        label = example[-1]
        countByLabels[label] = countByLabels.get(label, 0) + 1
    
    entropy = 0.0
    numberOfEntries = len(dataset)
    for ( _, value) in countByLabels.items():
        probability = float(value) / numberOfEntries
        entropy -= probability * math.log(probability, 2)

    return entropy

def loadDataset(filename):
    dataset = []
    labels = None
    with open(filename) as file:
        rows = csv.reader(file, delimiter=',')
        for row in rows:
            vector = []
            for i in range(0, len(row)):
                vector.append(str(row[i]))
            dataset.append(vector)
    labels = list(range(len(dataset[0])))
    labels = [ '@attribute V' + str(label) for label in labels ]
    return (dataset, labels)

def split(dataset, feature, value):
    datasetSplitted = []
    for example in dataset:
        if example[feature] == value :
            exampleSplitted = example[:feature]
            exampleSplitted.extend(example[feature+1:])
            datasetSplitted.append(exampleSplitted)
    return datasetSplitted

def chooseBestFeatureToSplit(dataset):
    numberOfFeatures = len(dataset[0])-1
    baseEntropy = shannonEntropy(dataset)
    bestInformationGain = 0.0
    bestFeatureToSplit = -1

    for i in range(numberOfFeatures):
        values = set([ example[i] for example in dataset ])
        newEntropy = 0.0
        for value in values:
            subDataset = split(dataset, i, value)
            probability = len(subDataset) / float(len(dataset))
            newEntropy += probability * shannonEntropy(subDataset)
        
        infoGain = baseEntropy - newEntropy
        if ( infoGain > bestInformationGain ):
            bestInformationGain = infoGain
            bestFeatureToSplit = i
    
    return bestFeatureToSplit

def majorityClass(classes):
    countByClass = dict()
    for clazz in classes:
        countByClass[clazz] = countByClass.get(clazz, 0) + 1
    return max(countByClass.items(), key=operator.itemgetter(1))[0]

def createTree(dataset, labels):
    classes = [ example[-1] for example in dataset ]
    
    if classes.count(classes[0]) == len(classes):
        return classes[0]
    
    if len(dataset[0]) == 1:
        return majorityClass(classes)
    
    bestFeatureToSplit = chooseBestFeatureToSplit(dataset)
    bestFeatureLabel = labels[bestFeatureToSplit]

    tree = { bestFeatureLabel : {} }
    del(labels[bestFeatureToSplit])

    values = set([ example[bestFeatureToSplit] for example in dataset ])
    for value in values:
        subLabels = labels[:]
        subExamples = split(dataset, bestFeatureToSplit, value)
        tree[bestFeatureLabel][value] = createTree(subExamples, subLabels)
    
    return tree

def loadTestset(filename):
    testset = []
    with open(filename) as file:
        rows = csv.reader(file, delimiter=',')
        for row in rows:
            vector = []
            for i in range(0, len(row)):
                vector.append(str(row[i]))
            testset.append(vector)
    return testset

def testExample(example, tree):
    if 'won' == tree or 'nowin' == tree:
        return tree

    attribute = list(tree.keys())[0]
    index_attribute = int(attribute.replace('@attribute V', '').strip()) - 1
    for (key, value) in tree[attribute].items():
        if example[index_attribute] == key:
            return testExample(example, value)

def saveClassification(example, classification):
    with open('classification.txt', 'a', newline='') as classification_file:
        classification_file.write(str(example) + ' => ' + str(classification) + '\n')

def clearClassificationFile():
     with open('classification.txt', 'w', newline='') as _ :
        pass

def testSample(sample, tree):
    clearClassificationFile()
    correctClassification = 0
    for example in sample:
        classification = testExample(example, tree)
        saveClassification(example, classification)
        if classification == example[-1]:
            correctClassification = correctClassification + 1
    
    lengthOfSample = len(sample)
    accuracy = float(correctClassification / lengthOfSample)
    errorRate = 1.0 - accuracy

    print('Number of cases  : ' + str(lengthOfSample))
    print('Accuracy         : ' + str(accuracy))
    print('Error Rate       : ' + str(errorRate))

def saveTree(tree):
    with open('tree.txt', 'w') as tree_file:
        json.dump(tree, tree_file, indent=4)

def main():
    (dataset, labels) = loadDataset('Xadrez-data.txt')
    tree = createTree(dataset, labels)
    saveTree(tree)

    sample = loadTestset('Xadrez-test.txt')
    testSample(sample, tree)

if __name__ == "__main__":
    main()