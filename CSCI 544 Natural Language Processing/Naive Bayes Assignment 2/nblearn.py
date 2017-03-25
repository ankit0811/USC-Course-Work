import sys;
import re;
import PorterStemmer1;
import removeStopWords as rsw;

def readTrainData():


    masterSet = [re.sub('[-!,.:]',' ',re.sub('[^a-zA-Z0-9-!,.: ]','',line.rstrip('\n').rstrip('\n'))) for line in open(trainTextFile)]
#    masterSet = [line.rstrip('\n') for line in open(trainTextFile)]
    masterLabel = [line.rstrip('\n').rstrip('\r') for line in open(trainLabelFile)]

    '''
    Distributing the data set into 2 (75-25) for Development and Testing Set
    '''

    developmentSet=[];
    testingSet=[];
    for i in range(len(masterSet)):
 #       if i%4!=0:
        developmentSet.append(masterSet[i]);
        '''        else:
            testingSet.append(masterSet[i]);
    print "Distribution of data(%d) to development set(%d) and testing set(%d)"%(len(masterSet), len(developmentSet), len(testingSet) )

        '''


    '''with open('testing.txt', 'w') as f:
        for value in testingSet:
            f.write('%s\n' % (value))
    '''


    developmentSetDict=dict();
    for i in range(len(developmentSet)):
        developmentSetDict[developmentSet[i].split(" ")[0]]=rsw.removeStopWords(developmentSet[i].lower().split(" ")[1:])

    print developmentSetDict["21jl365VxqszmTAJ29g0"]

    '''
    Creating dictionaries for master data set and label
    conatians key as the ID and value is a list of labels in case of labels and comments in case of text
    Lookup masterLabel Set and obtain the development label Set
    '''

    masterLabelDict=dict();
    developmentSetLabelDict=dict();
    deceptiveCount=0; truthfulCount=0; positiveCount=0; negativeCount=0;

    for i in range(len(masterLabel)):
        tempId=masterLabel[i].split(" ")[0]
        tempLabel=masterLabel[i].split(" ")[1:]
        masterLabelDict[tempId]=tempLabel
        if tempId in developmentSetDict:
            developmentSetLabelDict[tempId]=tempLabel
            if "deceptive" in tempLabel:
                deceptiveCount=deceptiveCount+1;
            if "truthful" in tempLabel:
                truthfulCount=truthfulCount+1;
            if "positive" in tempLabel:
                positiveCount=positiveCount+1;
            if "negative" in tempLabel:
                negativeCount=negativeCount+1;

    print "Distribution of development set acc to the lables \n" \
          "deceptiveCount %d truthfulCount %d positiveCount %d negativeCount %d" %(deceptiveCount, truthfulCount, positiveCount, negativeCount)
    tempDenominator=deceptiveCount + truthfulCount + positiveCount + negativeCount

    print "Hence the priors are \np(deceptive)=%f \np(truthful)=%f \np(positive)=%f \np(negative)=%f" %(float(deceptiveCount)/tempDenominator, (truthfulCount*1.0)/tempDenominator, (positiveCount*1.0)/tempDenominator, (negativeCount*1.0)/tempDenominator)

    with open('priors.txt','w') as f:
        f.write('%s:%f\n' % ("deceptive", float(deceptiveCount)/(deceptiveCount + truthfulCount)))
        f.write('%s:%f\n' % ("truthful", (truthfulCount*1.0)/(deceptiveCount + truthfulCount)))
        f.write('%s:%f\n' % ("positive", float(positiveCount)/(positiveCount + negativeCount)))
        f.write('%s:%f\n' % ("negative", float(negativeCount)/(positiveCount + negativeCount)))

    #print developmentSetDict

    featureCountDict=dict()
    count=0
    for id,finalFeatureList in developmentSetDict.iteritems():
        count=count+1
        for i in range(len(finalFeatureList)):
            countValue=[]
            if finalFeatureList[i] in featureCountDict.iterkeys():
                #deceptive, truthful, positive, negative
                countValue=featureCountDict[finalFeatureList[i]]
                #print "In featureCountDict"
            else:
                countValue=[0,0,0,0]
            if "deceptive" in developmentSetLabelDict[id]:
                countValue[0]=countValue[0]+1;
            if "truthful" in developmentSetLabelDict[id]:
                countValue[1]=countValue[1]+1;
            if "positive" in developmentSetLabelDict[id]:
                countValue[2]=countValue[2]+1;
            if "negative" in developmentSetLabelDict[id]:
                countValue[3]=countValue[3]+1;

            featureCountDict[finalFeatureList[i]]=countValue

        #print "iterationNo=",count
        #print len(featureCountDict)
        #print featureCountDict
        #exit(1)

    #print sorted(featureCountDict.items())
    getFeatureProb(featureCountDict)

def getFeatureProb(featureCountDict):
    #print featureCountDict.values()
    labelCounts=[sum(i) for i in zip(*featureCountDict.values())]


    finalDecpetiveCount=0; finalTruthfulCount=0; finalPositiveCount=0; finalNegativeCount=0;
    for word,featureCount in featureCountDict.iteritems():
        for i in range(len(featureCount)):
            featureCount[i]=float(featureCount[i]+1)/(labelCounts[i]+len(featureCountDict.keys()))
        featureCountDict[word]=featureCount


    writeDict(featureCountDict,'NBModel.txt')
    #print featureCountDict

    #print finalDecpetiveCount, finalTruthfulCount, finalPositiveCount, finalNegativeCount


def writeDict(dictWrite, fileName):
    with open(fileName, 'w') as f:
        for key, value in dictWrite.items():
            f.write('%s:%s\n' % (key, value))







def replaceAll(sentence, listOfStopWords):
    for i in listOfStopWords:
        sentence=sentence.replace(i,'')
    print sentence


def main():
    readTrainData()




print sys.argv
trainTextFile=sys.argv[1]
trainLabelFile=sys.argv[2]
P=PorterStemmer1.PorterStemmer1()
if __name__ == '__main__': main()