import pandas
import numpy as np
import re

Labels = set(
    ['Atelectasis', 'Consolidation', 'Edema', 'Pleural_Thickening', 'Infiltration', 'Mass', 'Nodule', 'Pneumonia',
     'Pneumothorax', 'Cardiomegaly', 'Effusion', 'Hernia',
     'Emphysema', 'Fibrosis', 'No Finding'])

def checkLabel(text, labels):
    findLabels = re.compile(r'([A-Z]\w*(?:\s[A-Z]\w*)?)')
    foundLabel = []
    for possible_labels in set(findLabels.findall(text)):
        if possible_labels in labels:
            foundLabel.append(possible_labels)
    return foundLabel


def getListLabels():

    listLabels = list(Labels)
    tempLabel = listLabels[13]
    listLabels.remove(tempLabel)
    listLabels.append(tempLabel)  # Ordering of the labels are now different (E, Ptho, Ed, C, P.T., Ate, Conso, Emphy,
    # P, Nod, M, Infilt, hernia, No finding)

    return listLabels

def thresholdLabels(threshold=3):
    colName = ['ImageIndex', 'FindingLabels', 'Followup', 'PatientID', 'PatientAge', 'PatientGender', 'ViewPosition',
               'OriginalImage', 'Height', 'OriginalImagePixelSpacing', 'y', 'temp']
    data = pandas.read_csv('Data_Entry_2017.csv', names=colName)

    findingLabels = data.FindingLabels.tolist()[1:]

    listLabels = getListLabels()

    oneHotLabels = np.zeros((len(findingLabels), 14))
    n = 0
    for i in range(len(findingLabels)):
        returnPathology = checkLabel(findingLabels[i], Labels)

        if len(returnPathology) < threshold and returnPathology[0] != 'No Finding':
            for m in range(len(returnPathology)):
                oneHotLabels[n, listLabels.index(returnPathology[m])] = 1


            n += 1

    thresholdLabels = oneHotLabels[:(n-1)]

    return thresholdLabels

