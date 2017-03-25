import sys;
import re;
import PorterStemmer1;
import removeStopWords as rsw;
import math as m;

def readTestFile(testTextFile):
    testFileList=[re.sub('[-!,.:]',' ',re.sub('[^a-zA-Z0-9-!,.: ]','',line.rstrip('\n').rstrip('\r'))) for line in open(testTextFile)]
    testSetDict=dict();
    for i in range(len(testFileList)):
        id=testFileList[i].split(" ")[0]
        value=rsw.removeStopWords(testFileList[i].split(" ")[1:])
        testSetDict[id]=value
        computeLabel(id, value)
    #print labelPrediction
    with open('nboutput.txt','w') as f:
        for key,value in labelPrediction.iteritems():
            f.write('%s %s %s\n' % (key, value[0], value[1]))
        f.close()



'''
    Read the prior probability stored by the learning model
'''
def readPriorProbabilities(priorFileName, priors):
    priorProbData=[line.rstrip('\n') for line in open(priorFileName)]

    for i in range(len(priorProbData)):
        priors[priorProbData[i].split(":")[0]]=priorProbData[i].split(":")[1]


def readWordProbabilities(modelFileName):
    wordProbData=[line.rstrip('\n') for line in open(modelFileName)]

    for i in range(len(wordProbData)):
        model[wordProbData[i].split(":")[0]]=wordProbData[i].split(":")[1]



def computeLabel(id, value):
    deceptiveP=m.log(float(priors["deceptive"]),10); truthFulP=m.log(float(priors["truthful"]),10); positiveP=m.log(float(priors["positive"]),10); negativeP=m.log(float(priors["negative"]),10);

    for i in range(len(value)):
        if value[i] in model.keys():
            modelProb=model[value[i]].replace("[","").replace("]","").split(",")

            if modelProb[0]>0:
                deceptiveP=deceptiveP+m.log(float(modelProb[0]),10)
            else:
                deceptiveP=deceptiveP+m.log(float(1)/len(model.values()),10)
            if modelProb[1]>0:
                truthFulP=truthFulP+m.log(float(modelProb[1]),10)
            else:
                truthFulP=truthFulP+m.log(float(1)/len(model.values()),10)
            if modelProb[2]>0:
                positiveP=positiveP+m.log(float(modelProb[2]),10)
            else:
                positiveP=positiveP+m.log(float(1)/len(model.values()),10)
            if modelProb[3]>0:
                negativeP=negativeP+m.log(float(modelProb[3]),10)
            else:
                negativeP=negativeP+m.log(float(1)/len(model.values()),10)



    outLabel=[]
    if deceptiveP>truthFulP:
        outLabel.append("deceptive")
    else:
        outLabel.append("truthful")
    if positiveP>negativeP:
        outLabel.append("positive")
    else:
        outLabel.append("negative")
    labelPrediction[id]=outLabel



def main():
    readPriorProbabilities('priors.txt',priors)
    readWordProbabilities('NBModel.txt');
    readTestFile(testTextFile)




print sys.argv
testTextFile=sys.argv[1]
list1=[1,2,3]

P=PorterStemmer1.PorterStemmer1()
priors=dict()
labelPrediction=dict()
model=dict()
main()