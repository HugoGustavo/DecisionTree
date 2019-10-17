import sys
import csv
import random

def writeFile(sample):
    with open('Xadrez-test.txt', 'w', newline='') as test_data_file:
        writer = csv.writer(test_data_file)
        writer.writerows(sample)

def generateExample():
    example = []
    # Atributo 1-12
    for _ in range(12):
        example.append( 'f' if random.random() < 0.5 else 't' )

    # Atributo 13
    example.append ( 'g' if random.random() < 0.5 else 'l' )

    # atributo 14
    example.append ( 'f' if random.random() < 0.5 else 't' )

    #Atributo 15
    value = random.random()
    if ( value < 0.33 ):
        example.append ('b')
    elif (value < 0.66 ):
        example.append('n')
    else:
        example.append('w')

    #Atributo 16-35
    for _ in range(20):
        example.append( 'f' if random.random() < 0.5 else 't' )

    # Atributo 36
    example.append ( 't' if random.random() < 0.5 else 'n' )

    # Atributo 37
    example.append ( 'nowin' if random.random() < 0.5 else 'won' )

    return example

def generateSample(size):
    sample = []
    for _ in range(size):
        sample.append(generateExample())
    return sample

if __name__ == "__main__":
    size = int(sys.argv[1])
    sample = generateSample(size)
    writeFile(sample)